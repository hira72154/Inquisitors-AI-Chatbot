"""Store embeddings in ChromaDB and parse chunks."""

import chromadb
from pathlib import Path
from embedder import EmbeddingGenerator
import yaml
from typing import List, Dict

def parse_chunk_file(file_path: str) -> Dict:
    """Parse a .md chunk file with YAML frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by --- to get frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    # Parse YAML
    frontmatter = yaml.safe_load(parts[1].strip())
    markdown_content = parts[2].strip()
    
    return {
        'chunk_id': frontmatter.get('chunk_id', 'unknown'),
        'source': frontmatter.get('source', 'unknown'),
        'section': frontmatter.get('section', 'general'),
        'doc_id': frontmatter.get('doc_id', 'unknown'),
        'text': markdown_content,
        'metadata': {
            'source': frontmatter.get('source', 'unknown'),
            'section': frontmatter.get('section', 'general'),
            'doc_id': frontmatter.get('doc_id', 'unknown')
        }
    }

def load_all_chunks(chunks_folder: str) -> List[Dict]:
    """Load all chunk .md files."""
    chunks = []
    chunks_path = Path(chunks_folder)
    
    md_files = sorted(chunks_path.glob('*.md'))
    print(f"Found {len(md_files)} chunk files")
    
    for md_file in md_files:
        try:
            chunk = parse_chunk_file(str(md_file))
            if chunk:
                chunks.append(chunk)
                print(f"✅ {md_file.name}")
        except Exception as e:
            print(f"❌ {md_file.name}: {e}")
    
    return chunks

def store_in_chromadb(chunks: List[Dict], embedder: EmbeddingGenerator):
    """Store chunks with embeddings in ChromaDB."""
    
    # Create/connect to ChromaDB
    persist_dir = "./chroma_db"
    Path(persist_dir).mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=persist_dir)
    
    # Get collection
    collection = client.get_or_create_collection(
        name="maa_knowledge",
        metadata={"hnsw:space": "cosine"}
    )
    print(f"\n✅ Connected to ChromaDB at: {persist_dir}")
    
    # Extract data
    texts = [chunk['text'] for chunk in chunks]
    ids = [chunk['chunk_id'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]
    
    # Generate embeddings
    print(f"\n🔢 Generating embeddings for {len(texts)} chunks...")
    embeddings = embedder.embed_batch(texts)
    embeddings_lists = [emb.tolist() for emb in embeddings]
    
    # Store in ChromaDB
    print(f"💾 Storing in ChromaDB...")
    collection.add(
        ids=ids,
        embeddings=embeddings_lists,
        metadatas=metadatas,
        documents=texts
    )
    
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
    print(f"✅ Collection size: {collection.count()} documents")

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("EMBEDDINGS & CHROMADB SETUP")
    print("="*60)
    
    # Step 1: Load chunks
    print("\n1️⃣ Loading chunks...")
    chunks = load_all_chunks("./chunks")
    
    if not chunks:
        print("❌ No chunks found in ./chunks/")
        exit(1)
    
    print(f"\n✅ Loaded {len(chunks)} chunks")
    
    # Step 2: Initialize embedder
    print("\n2️⃣ Initializing embedder...")
    embedder = EmbeddingGenerator()
    
    # Step 3: Store in ChromaDB
    print("\n3️⃣ Storing in ChromaDB...")
    store_in_chromadb(chunks, embedder)
    
    print("\n" + "="*60)
    print("✅ YOUR JOB DONE!")
    print("="*60)
    print("\n📁 Created: chroma_db/ (the database)")
    print("🚀 Ready for retrieval member to use")