"""Load documentation chunks, create embeddings, and store them in ChromaDB."""

import chromadb
from pathlib import Path
from typing import List, Dict, Optional
import yaml

from embedder import EmbeddingGenerator


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_DIR = BASE_DIR / "embeddings" / "chunks"
CHROMA_DIR = BASE_DIR / "embeddings" / "chroma_db"


# ============================================================
# PARSE CHUNK
# ============================================================

def parse_chunk_file(file_path: Path) -> Optional[Dict]:
    """Parse a Markdown chunk containing YAML frontmatter."""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        parts = content.split("---", 2)

        if len(parts) < 3:
            print(f"⚠️ Invalid chunk format: {file_path.name}")
            return None

        frontmatter = yaml.safe_load(parts[1].strip()) or {}
        markdown_content = parts[2].strip()

        original_chunk_id = frontmatter.get(
            "chunk_id",
            file_path.stem
        )

        # IMPORTANT:
        # Make ID unique using filename
        unique_chunk_id = f"{file_path.stem}__{original_chunk_id}"

        return {
            "chunk_id": unique_chunk_id,

            "original_chunk_id": original_chunk_id,

            "source": frontmatter.get(
                "source",
                "unknown"
            ),

            "section": frontmatter.get(
                "section",
                "general"
            ),

            "doc_id": frontmatter.get(
                "doc_id",
                "unknown"
            ),

            "text": markdown_content,

            "metadata": {
                "source": str(
                    frontmatter.get(
                        "source",
                        "unknown"
                    )
                ),

                "section": str(
                    frontmatter.get(
                        "section",
                        "general"
                    )
                ),

                "doc_id": str(
                    frontmatter.get(
                        "doc_id",
                        "unknown"
                    )
                ),

                "original_chunk_id": str(
                    original_chunk_id
                ),

                "file_name": file_path.name
            }
        }

    except Exception as e:
        print(
            f"❌ Error parsing {file_path.name}: {e}"
        )
        return None


# ============================================================
# LOAD ALL CHUNKS
# ============================================================

def load_all_chunks() -> List[Dict]:

    print("\n📁 Chunks directory:")
    print(CHUNKS_DIR)

    if not CHUNKS_DIR.exists():
        print("❌ Chunks directory does not exist!")
        return []

    md_files = sorted(
        CHUNKS_DIR.glob("*.md")
    )

    print(
        f"\n📄 Found {len(md_files)} Markdown chunk files"
    )

    chunks = []

    for md_file in md_files:

        chunk = parse_chunk_file(md_file)

        if chunk:
            chunks.append(chunk)

    print(
        f"\n✅ Successfully loaded {len(chunks)} chunks"
    )

    return chunks


# ============================================================
# CHECK DUPLICATE IDS
# ============================================================

def check_duplicate_ids(chunks: List[Dict]):

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    duplicates = {
        chunk_id
        for chunk_id in ids
        if ids.count(chunk_id) > 1
    }

    if duplicates:

        print("\n⚠️ Duplicate IDs found:")

        for duplicate in duplicates:
            print(
                f"   - {duplicate}"
            )

        return False

    print(
        "✅ All chunk IDs are unique"
    )

    return True


# ============================================================
# STORE IN CHROMADB
# ============================================================

def store_in_chromadb(
    chunks: List[Dict],
    embedder: EmbeddingGenerator
):

    print("\n" + "=" * 60)
    print("CHROMADB SETUP")
    print("=" * 60)

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"\n📁 ChromaDB path:\n{CHROMA_DIR}"
    )

    # Connect to ChromaDB
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Get/create collection
    collection = client.get_or_create_collection(
        name="maa_knowledge",
        metadata={
            "hnsw:space": "cosine"
        }
    )

    print(
        f"📊 Existing collection count: "
        f"{collection.count()}"
    )

    # --------------------------------------------------------
    # Check IDs
    # --------------------------------------------------------

    if not check_duplicate_ids(chunks):

        raise ValueError(
            "Duplicate chunk IDs detected. "
            "Please check your chunk files."
        )

    # --------------------------------------------------------
    # Prepare data
    # --------------------------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    print(
        f"\n🔢 Generating embeddings for "
        f"{len(texts)} chunks..."
    )

    embeddings = embedder.embed_batch(
        texts
    )

    embeddings_lists = [
        embedding.tolist()
        for embedding in embeddings
    ]

    # --------------------------------------------------------
    # Store / Update
    # --------------------------------------------------------

    print(
        "\n💾 Storing chunks in ChromaDB..."
    )

    collection.upsert(
        ids=ids,
        embeddings=embeddings_lists,
        metadatas=metadatas,
        documents=texts
    )

    print(
        f"\n✅ Stored/updated {len(chunks)} chunks"
    )

    print(
        f"✅ Total ChromaDB documents: "
        f"{collection.count()}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("MAA DOCUMENTATION → EMBEDDINGS → CHROMADB")
    print("=" * 60)

    # 1. Load chunks
    print(
        "\n1️⃣ Loading documentation chunks..."
    )

    chunks = load_all_chunks()

    if not chunks:

        print(
            "\n❌ No chunks found."
        )

        print(
            f"Make sure your .md files are inside:\n"
            f"{CHUNKS_DIR}"
        )

        raise SystemExit(1)

    # 2. Check IDs
    print(
        "\n2️⃣ Checking chunk IDs..."
    )

    check_duplicate_ids(chunks)

    # 3. Load embedding model
    print(
        "\n3️⃣ Loading embedding model..."
    )

    embedder = EmbeddingGenerator()

    # 4. Store embeddings
    print(
        "\n4️⃣ Storing embeddings in ChromaDB..."
    )

    store_in_chromadb(
        chunks,
        embedder
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "🎉 DONE!"
    )

    print(
        "=" * 60
    )

    print(
        "\nYour complete documentation is now "
        "available for semantic retrieval."
    )