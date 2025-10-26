"""
RAG Pipeline Module
Handles embedding generation, FAISS indexing, and retrieval
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Tuple
import pickle
import os


class RAGPipeline:
    """Retrieval-Augmented Generation Pipeline"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2', cache_dir=None):
        """
        Initialize RAG Pipeline
        
        Args:
            model_name (str): Name of the sentence transformer model
            cache_dir (str): Directory to cache models (optional)
        """
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.model = None
        self.index = None
        self.chunks = []
        self.embeddings = None
        
    def load_model(self):
        """Load the sentence transformer model"""
        if self.model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name, cache_folder=self.cache_dir)
            print(f"✅ Model loaded successfully")
            print(f"   Device: {self.model.device}")
            print(f"   Max sequence length: {self.model.max_seq_length}")
        return self.model
    
    def generate_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """
        Generate embeddings for chunks
        
        Args:
            chunks (list): List of chunk dictionaries with 'text' key
            
        Returns:
            np.ndarray: Array of embeddings
        """
        if self.model is None:
            self.load_model()
        
        # Extract text from chunks
        texts = [chunk['text'] for chunk in chunks]
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        
        # Convert to float32 for FAISS
        embeddings = embeddings.astype('float32')
        
        print(f"✅ Generated embeddings: {embeddings.shape}")
        
        # Store embeddings
        self.embeddings = embeddings
        
        return embeddings
    
    def create_index(self, embeddings: np.ndarray = None):
        """
        Create FAISS index from embeddings
        
        Args:
            embeddings (np.ndarray): Array of embeddings (optional, uses stored if None)
        """
        if embeddings is None:
            embeddings = self.embeddings
        
        if embeddings is None:
            raise ValueError("No embeddings provided or generated")
        
        # Get dimension
        dimension = embeddings.shape[1]
        
        print(f"Creating FAISS index...")
        print(f"   Dimension: {dimension}")
        print(f"   Number of vectors: {len(embeddings)}")
        
        # Create index (using L2 distance, normalized embeddings make it equivalent to cosine)
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        print(f"✅ FAISS index created with {self.index.ntotal} vectors")
        
        return self.index
    
    def build_index(self, chunks: List[Dict]) -> faiss.Index:
        """
        Complete pipeline: generate embeddings and build index
        
        Args:
            chunks (list): List of chunk dictionaries
            
        Returns:
            faiss.Index: FAISS index
        """
        # Store chunks
        self.chunks = chunks
        
        # Generate embeddings
        embeddings = self.generate_embeddings(chunks)
        
        # Create index
        index = self.create_index(embeddings)
        
        return index
    
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve top-k most relevant chunks for a query
        
        Args:
            query (str): Search query
            k (int): Number of chunks to retrieve
            
        Returns:
            list: List of retrieved chunks with scores
        """
        if self.model is None:
            self.load_model()
        
        if self.index is None:
            raise ValueError("Index not created. Call build_index() first")
        
        # Generate query embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype('float32')
        
        # Search in index
        distances, indices = self.index.search(query_embedding, min(k, len(self.chunks)))
        
        # Prepare results
        results = []
        for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk['retrieval_score'] = float(1 / (1 + distance))  # Convert distance to similarity score
                chunk['distance'] = float(distance)
                chunk['rank'] = i + 1
                results.append(chunk)
        
        return results
    
    def retrieve_context(self, query: str, k: int = 3, max_tokens: int = 1500) -> str:
        """
        Retrieve and combine relevant chunks as context
        
        Args:
            query (str): Search query
            k (int): Number of chunks to retrieve
            max_tokens (int): Maximum tokens in combined context
            
        Returns:
            str: Combined context text
        """
        # Retrieve chunks
        results = self.retrieve(query, k)
        
        # Combine chunks
        context_parts = []
        total_tokens = 0
        
        for result in results:
            chunk_tokens = result.get('token_count', 0)
            
            # Check if adding this chunk exceeds limit
            if total_tokens + chunk_tokens > max_tokens:
                break
            
            context_parts.append(result['text'])
            total_tokens += chunk_tokens
        
        # Join with separators
        context = "\n\n---\n\n".join(context_parts)
        
        return context
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the RAG pipeline
        
        Returns:
            dict: Statistics
        """
        stats = {
            'model_name': self.model_name,
            'model_loaded': self.model is not None,
            'index_created': self.index is not None,
            'num_chunks': len(self.chunks),
            'num_embeddings': len(self.embeddings) if self.embeddings is not None else 0,
            'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else 0,
            'index_size': self.index.ntotal if self.index is not None else 0
        }
        
        if self.model is not None:
            stats['model_device'] = str(self.model.device)
            stats['max_seq_length'] = self.model.max_seq_length
        
        return stats
    
    def save_index(self, filepath: str):
        """
        Save FAISS index and chunks to disk
        
        Args:
            filepath (str): Path to save (without extension)
        """
        if self.index is None:
            raise ValueError("No index to save")
        
        # Save FAISS index
        index_path = f"{filepath}.index"
        faiss.write_index(self.index, index_path)
        
        # Save chunks and embeddings
        data_path = f"{filepath}.pkl"
        with open(data_path, 'wb') as f:
            pickle.dump({
                'chunks': self.chunks,
                'embeddings': self.embeddings,
                'model_name': self.model_name
            }, f)
        
        print(f"✅ Index saved to {index_path}")
        print(f"✅ Data saved to {data_path}")
    
    def load_index(self, filepath: str):
        """
        Load FAISS index and chunks from disk
        
        Args:
            filepath (str): Path to load (without extension)
        """
        # Load FAISS index
        index_path = f"{filepath}.index"
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        self.index = faiss.read_index(index_path)
        
        # Load chunks and embeddings
        data_path = f"{filepath}.pkl"
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
            self.chunks = data['chunks']
            self.embeddings = data['embeddings']
            self.model_name = data['model_name']
        
        print(f"✅ Index loaded from {index_path}")
        print(f"✅ Data loaded from {data_path}")
        print(f"   Chunks: {len(self.chunks)}")
        print(f"   Index size: {self.index.ntotal}")


# Convenience functions
def create_rag_pipeline(chunks: List[Dict], model_name='all-MiniLM-L6-v2') -> RAGPipeline:
    """
    Create and build a RAG pipeline
    
    Args:
        chunks (list): List of chunk dictionaries
        model_name (str): Embedding model name
        
    Returns:
        RAGPipeline: Initialized pipeline
    """
    pipeline = RAGPipeline(model_name=model_name)
    pipeline.build_index(chunks)
    return pipeline


def retrieve_relevant_chunks(pipeline: RAGPipeline, query: str, k: int = 5) -> List[Dict]:
    """
    Retrieve relevant chunks from pipeline
    
    Args:
        pipeline (RAGPipeline): RAG pipeline instance
        query (str): Search query
        k (int): Number of chunks to retrieve
        
    Returns:
        list: Retrieved chunks
    """
    return pipeline.retrieve(query, k)