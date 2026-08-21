from pathlib import Path
import re
import json

KNOWLEDGE_FOLDER = Path("KNOWLEDGE_source")


def read_metadata_and_text(file_path):
    content = file_path.read_text(encoding="utf-8")

    source_match = re.search(r"^source:\s*(.+)$", content, re.MULTILINE)
    section_match = re.search(r"^section:\s*(.+)$", content, re.MULTILINE)
    doc_id_match = re.search(r"^doc_id:\s*(.+)$", content, re.MULTILINE)

    source = source_match.group(1).strip() if source_match else ""
    section = section_match.group(1).strip() if section_match else ""
    doc_id = doc_id_match.group(1).strip() if doc_id_match else ""

    return {
        "text": content,
        "source": source,
        "section": section,
        "doc_id": doc_id
    }


def main():
    documents = []

    for file_path in KNOWLEDGE_FOLDER.glob("*.md"):
        document = read_metadata_and_text(file_path)
        documents.append(document)

    output_file = Path("ingested_data.json")
    output_file.write_text(
        json.dumps(documents, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Processed {len(documents)} files.")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()