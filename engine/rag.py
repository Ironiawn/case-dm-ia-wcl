from math import sqrt

from engine import openai_client


documents = []


def cosine_similarity(vector_a: list[float], vector_b: list[float]):
    """
    Calcula a similaridade entre dois vetores.
    """
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = sqrt(sum(a * a for a in vector_a))
    norm_b = sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot_product / (norm_a * norm_b)


def split_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    """
    Quebra um texto grande em pedaços menores.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def prepare_documents(items: list[dict]):
    """
    Transforma textos grandes em vários pedaços menores.
    """
    prepared_documents = []

    for item in items:
        text = item["text"]
        file_name = item["file_name"]
        page = item["page"]
        chunks = split_text(text)

        for index, chunk in enumerate(chunks, start=1):
            prepared_documents.append(
                {
                    "text": chunk,
                    "file_name": file_name,
                    "page": page,
                    "chunk_id": index,
                }
            )

    return prepared_documents


def index_documents(items: list[dict]):
    """
    Cria os embeddings dos textos e guarda tudo em memória.
    """
    global documents

    if not items:
        documents = []
        return

    prepared_documents = prepare_documents(items)
    texts = [item["text"] for item in prepared_documents]
    embeddings = openai_client.create_embeddings(texts)
    documents = []

    for item, embedding in zip(prepared_documents, embeddings):
        documents.append(
            {
                "text": item["text"],
                "file_name": item["file_name"],
                "page": item["page"],
                "chunk_id": item["chunk_id"],
                "embedding": embedding,
            }
        )


def has_documents():
    """
    Informa se o RAG já possui documentos indexados.
    """
    return len(documents) > 0


def retrieve_context(question: str, top_k: int = 3):
    """
    Busca os textos mais parecidos com a pergunta.
    """
    if not documents:
        return {
            "context": "",
            "audit": [],
        }

    question_embedding = openai_client.create_embedding(question)
    scored_documents = []

    for document in documents:
        score = cosine_similarity(question_embedding, document["embedding"])
        scored_documents.append(
            {
                "score": score,
                "text": document["text"],
                "file_name": document["file_name"],
                "page": document["page"],
                "chunk_id": document["chunk_id"],
            }
        )

    scored_documents.sort(reverse=True, key=lambda item: item["score"])
    best_documents = scored_documents[:top_k]
    best_texts = [item["text"] for item in best_documents]

    return {
        "context": "\n\n".join(best_texts),
        "audit": best_documents,
    }
