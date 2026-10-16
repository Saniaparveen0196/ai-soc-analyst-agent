
import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_FILE = PROJECT_ROOT / "data" / "security_knowledge.json"

_embedding_model = None
_vector_store = None


def get_vector_store():
    global _embedding_model, _vector_store

    if _vector_store is not None:
        return _vector_store

    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        knowledge = json.load(file)

    documents = [
        Document(
            page_content=(
                f"Topic: {item['topic']}\n"
                f"Keywords: {', '.join(item['keywords'])}\n"
                f"Guidance: {item['guidance']}"
            ),
            metadata={"topic": item["topic"]},
        )
        for item in knowledge
    ]

    _embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    _vector_store = FAISS.from_documents(
        documents,
        _embedding_model,
    )

    return _vector_store


def search_security_knowledge_semantic(
    query: str,
    k: int = 2,
) -> list[dict]:
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)

    return [
        {
            "topic": document.metadata["topic"],
            "content": document.page_content,
        }
        for document in results
    ]


if __name__ == "__main__":
    query = "Repeated password failures may indicate automated credential guessing"

    results = search_security_knowledge_semantic(query)

    print("\n=== SEMANTIC SEARCH RESULTS ===")
    for result in results:
        print("\nTopic:", result["topic"])
        print(result["content"])
