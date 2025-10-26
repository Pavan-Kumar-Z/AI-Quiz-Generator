┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Python is a high-level programming language. It was       │
│  created by Guido van Rossum in 1991. Python emphasizes    │
│  code readability and simplicity. The language supports    │
│  multiple programming paradigms including object-oriented, │
│  functional, and procedural programming. Python has a      │
│  comprehensive standard library and a large ecosystem.     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
````

### After Chunking (500 tokens, 100 overlap)
````
┌──────────────────────────────────┐
│ Chunk 1 (250 tokens)             │
│                                  │
│ Python is a high-level           │
│ programming language. It was     │
│ created by Guido van Rossum...   │
│                                  │
│ [Last 100 tokens overlap →]     │
└──────────────────────────────────┘
                ↓
┌──────────────────────────────────┐
│ [← 100 tokens overlap]          │
│                                  │
│ Chunk 2 (240 tokens)             │
│                                  │
│ ...created by Guido van Rossum   │
│ in 1991. Python emphasizes...    │
│                                  │
│ [Last 100 tokens overlap →]     │
└──────────────────────────────────┘
                ↓
┌──────────────────────────────────┐
│ [← 100 tokens overlap]          │
│                                  │
│ Chunk 3 (230 tokens)             │
│                                  │
│ ...code readability and          │
│ simplicity. The language...      │
│                                  │
└──────────────────────────────────┘


{
  "chunk_id": 0,
  "text": "Python is a high-level programming...",
  "char_count": 783,
  "token_count": 189,
  "metadata": {
    "source_file": "document.txt",
    "format": "txt"
  }
}
````

## Why Overlap Matters

### Without Overlap ❌
````
[Chunk 1: "...programming language."]
[Chunk 2: "Python emphasizes..."]
````
Context lost between chunks!

### With Overlap ✅
````
[Chunk 1: "...programming language. Python emphasizes..."]
[Chunk 2: "...programming language. Python emphasizes..."]
````
Context preserved across chunks!

## Token Counting
````
Text: "Python is great"
Characters: 15
Tokens: ~3-4

Why tokens?
- AI models work with tokens
- More accurate than characters
- Consistent with model limits
````

## Chunk Flow
````
Document Upload
      ↓
Text Extraction (PyMuPDF/docx)
      ↓
Text Cleaning
      ↓
Token Counting (tiktoken)
      ↓
Chunk Creation (langchain)
      ↓
Overlap Application
      ↓
Validation
      ↓
Storage (in-memory)
      ↓
Ready for RAG Pipeline


# Optimal for Phi-3-mini (4k context)
CHUNK_SIZE = 500 tokens
CHUNK_OVERLAP = 100 tokens

# Ensures:
- Each chunk fits in model
- Enough overlap for context
- Efficient retrieval
- Good question generation