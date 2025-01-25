import json
import chromadb
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parents[1]
chroma = chromadb.PersistentClient(path=str(BASE_DIR / "data" / "chroma.db"))


def create_collection(name: str) -> None:
    chroma.create_collection(name)


def get_first_collection() -> str:
    return chroma.list_collections()[0]


def add_document(
        documents: list = None, metadata: list[dict] = None, ids: list = None, collection: str = None
) -> None | str:
    """Add documents to the collection.

    When not specifying embedding model to collection.add(...) chroma implements a default model "all-minilm-l6-v2".

    Args:
        documents (list, optional): List of documents to add. Defaults to None although it is mandatory.
        metadata (list[dict], optional): List of metadata for each document. Defaults to None.
        ids (list, optional): List of ids for each document. Defaults to None.
        collection (str, optional): Name of the collection to add the documents to. Defaults to None.
    """
    if not documents:
        return "No documents provided"

    ids = ids or [f"doc {i+1}" for i in range(len(documents))]

    collection = collection or get_first_collection()
    collection_store = chroma.get_collection(collection)
    collection_store.add(documents=documents, metadatas=metadata, ids=ids)


def query_collection(query_text: str, n_results: int = 5, collection: str = None) -> dict:
    """Query the collection for similar documents.

    Args:
        query_text (str): List of query texts.
        n_results (int): Number of results to return. Defaults to top 5.
        collection (str): Name of the collection to query.

    Returns:
        list: List of results.
    """
    collection = collection or get_first_collection()
    collection_store = chroma.get_collection(collection)
    return collection_store.query(query_texts=query_text, n_results=n_results)


def populate_with_default_data(collection: str):
    with open(BASE_DIR / "data/recipes.json", "r") as f:
        data = json.load(f)
    add_document(documents=data, collection=collection)


if __name__ == "__main__":
    create_collection("collection-name")
    populate_with_default_data("collection-name")

    # from pprint import pprint
    # result = query_collection("I like seafood!", collection="collection-name")
    # pprint(result)
