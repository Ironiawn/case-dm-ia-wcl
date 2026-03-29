from engine import openai_client

tag_sessao_encerrada = "[ENCERRAR_SESSAO]"


def behave(instructions: str, prompt: str, context: str = "", session_history: str = ""):
    """
    Inicia o agente com as instruções fornecidas.
    """
    full_prompt = prompt

    if context or session_history:
        full_prompt = f"""
Use o contexto da sessão e o contexto recuperado abaixo para responder.
Se a resposta não estiver no contexto, diga isso com clareza.

HISTÓRICO DA SESSÃO:
{session_history}

CONTEXTO:
{context}

PERGUNTA:
{prompt}
""".strip()

    return openai_client.generate_response(
        prompt=full_prompt,
        instructions=instructions,
    )
