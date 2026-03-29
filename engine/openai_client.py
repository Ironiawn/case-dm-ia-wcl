import os

from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model_embedding = os.getenv("OPENAI_EMBEDDING_MODEL")
model_chat = os.getenv("OPENAI_CHAT_MODEL")

if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env.")
if not model_embedding:
    raise ValueError("A variável OPENAI_EMBEDDING_MODEL não foi encontrada no arquivo .env.")
if not model_chat:
    raise ValueError("A variável OPENAI_CHAT_MODEL não foi encontrada no arquivo .env.")

client = OpenAI(api_key=api_key)


def generate_response(prompt: str, instructions: str | None = None):
    """
    Gera uma resposta usando a API Responses da OpenAI.
    """
    request_data = {
        "model": model_chat,
        "input": prompt,
    }

    if instructions:
        request_data["instructions"] = instructions

    response = client.responses.create(**request_data)
    return response.output_text


def create_embedding(text: str):
    """
    Cria o embedding de um texto.
    """
    response = client.embeddings.create(
        model=model_embedding,
        input=text,
    )
    return response.data[0].embedding


def create_embeddings(texts: list[str]):
    """
    Cria embeddings para uma lista de textos.
    """
    response = client.embeddings.create(
        model=model_embedding,
        input=texts,
    )
    return [item.embedding for item in response.data]
