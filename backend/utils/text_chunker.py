"""
Text Chunker Module
Splits large documents into smaller chunks for processing
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
import tiktoken


class TextChunker:
    """Handles text chunking for document processing"""
    
    def __init__(self, chunk_size=500, chunk_overlap=100, encoding_name="cl100k_base"):
        """
        Initialize the text chunker
        
        Args:
            chunk_size (int): Maximum size of each chunk in tokens
            chunk_overlap (int): Number of overlapping tokens between chunks
            encoding_name (str): Tokenizer encoding to use
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding_name = encoding_name
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except:
            # Fallback to a simple character-based estimate
            self.encoding = None
        
        # Initialize the text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self._token_length,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def _token_length(self, text: str) -> int:
        """
        Calculate the token length of text
        
        Args:
            text (str): Input text
            
        Returns:
            int: Number of tokens
        """
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Rough estimate: ~4 characters per token
            return len(text) // 4
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into chunks
        
        Args:
            text (str): Text to chunk
            metadata (dict): Optional metadata to attach to each chunk
            
        Returns:
            list: List of chunk dictionaries
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Split the text
        chunks = self.text_splitter.split_text(text)
        
        # Create chunk objects with metadata
        chunk_objects = []
        for i, chunk in enumerate(chunks):
            chunk_obj = {
                'chunk_id': i,
                'text': chunk,
                'char_count': len(chunk),
                'token_count': self._token_length(chunk),
                'metadata': metadata or {}
            }
            chunk_objects.append(chunk_obj)
        
        return chunk_objects
    
    def get_chunk_stats(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about the chunks
        
        Args:
            chunks (list): List of chunk dictionaries
            
        Returns:
            dict: Statistics about chunks
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'total_tokens': 0,
                'total_chars': 0,
                'avg_tokens_per_chunk': 0,
                'avg_chars_per_chunk': 0
            }
        
        total_tokens = sum(chunk['token_count'] for chunk in chunks)
        total_chars = sum(chunk['char_count'] for chunk in chunks)
        
        return {
            'total_chunks': len(chunks),
            'total_tokens': total_tokens,
            'total_chars': total_chars,
            'avg_tokens_per_chunk': round(total_tokens / len(chunks), 2),
            'avg_chars_per_chunk': round(total_chars / len(chunks), 2),
            'min_tokens': min(chunk['token_count'] for chunk in chunks),
            'max_tokens': max(chunk['token_count'] for chunk in chunks)
        }
    
    def preview_chunks(self, chunks: List[Dict], max_preview_length=100) -> List[str]:
        """
        Get preview of each chunk
        
        Args:
            chunks (list): List of chunk dictionaries
            max_preview_length (int): Max length of preview
            
        Returns:
            list: List of chunk previews
        """
        previews = []
        for chunk in chunks:
            text = chunk['text']
            if len(text) > max_preview_length:
                preview = text[:max_preview_length] + "..."
            else:
                preview = text
            previews.append(preview)
        
        return previews
    
    def validate_chunks(self, chunks: List[Dict]) -> tuple:
        """
        Validate that chunks are suitable for processing
        
        Args:
            chunks (list): List of chunk dictionaries
            
        Returns:
            tuple: (is_valid, message)
        """
        if not chunks or len(chunks) == 0:
            return False, "No chunks created"
        
        # Check if any chunks are too small
        min_token_threshold = 10
        small_chunks = [c for c in chunks if c['token_count'] < min_token_threshold]
        
        if len(small_chunks) == len(chunks):
            return False, "All chunks are too small (less than 10 tokens)"
        
        # Check if chunks are too large
        max_token_threshold = self.chunk_size * 1.5
        large_chunks = [c for c in chunks if c['token_count'] > max_token_threshold]
        
        if large_chunks:
            return False, f"Some chunks exceed maximum size ({max_token_threshold} tokens)"
        
        return True, "Chunks are valid"


# Utility function for easy import
def chunk_text(text: str, chunk_size=500, chunk_overlap=100, metadata=None):
    """
    Convenience function to chunk text
    
    Args:
        text (str): Text to chunk
        chunk_size (int): Maximum chunk size in tokens
        chunk_overlap (int): Overlap between chunks
        metadata (dict): Optional metadata
        
    Returns:
        list: List of chunks
    """
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunker.chunk_text(text, metadata)