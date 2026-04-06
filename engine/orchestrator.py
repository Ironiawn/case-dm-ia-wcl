import os
import re
from engine import agent, rag
from pypdf import PdfReader
import config

instruction_data_cache = None
knowledge_data_cache = None


def orchestrate(agentId: int, user_question: str, session_history: str = ""):
    """
    Orquestrar o funcionamento end-to-end do sistema de agentes
    """

    instruction_data = load_instruction_data()
    clean_question = hide_sensitive_data(user_question)
    clean_history = hide_sensitive_data(session_history)

    # Obtém o arquivo MD de comportamentos do agente
    agent_file = pick_agent(agentId)
    agent_data = instruction_data["files"].get(agent_file)

    if agent_file == "-1":
        return {
            "answer": "Selecione um agente válido.",
            "audit": [],
        }
    else:
        if is_out_of_scope(agentId, clean_question):
            return {
                "answer": "Esse tema está fora do escopo deste agente. Use 'trocar' para mudar de agente.",
                "audit": [],
            }

        # Colocar o que o agente deve fazer e suas instruções comportamentais
        if not rag.has_documents():
            rag.index_documents(load_knowledge_data())

        agent_behaviour = instruction_data["rules"] + "\n" + agent_data
        rag_result = rag.retrieve_context(clean_question)
        answer = agent.behave(agent_behaviour, clean_question, rag_result["context"], clean_history)

        return {
            "answer": answer,
            "audit": rag_result["audit"],
        }

        
def pick_agent(agentId: int):
    """
    Obtém o arquivo MD de comportamentos do agente
    """
    # Avaliar agente a ser utilizado
    if agentId == 1:
        # Agente responsável por Anti-Fraude
        return os.path.join(config.get_project_root(), "agents", "anti_fraude.md")
    elif agentId == 2:
        # Agente responsável por Soluções
        return os.path.join(config.get_project_root(), "agents", "solucoes.md")
    else:
        return "-1" # Aqui não encontramos o agente, ou seja, o agenteId é inválido
    

def load_instruction_data():
    """
    Lê rules e agents como instrução.
    """
    global instruction_data_cache

    if instruction_data_cache is not None:
        return instruction_data_cache

    files = {}
    rules = ""

    for folder in ["rules", "agents"]:
        folder_path = os.path.join(config.get_project_root(), folder)
        file_names = os.listdir(folder_path)

        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            text = open(file_path, "r", encoding="utf-8").read()
            files[file_path] = text

            if folder == "rules":
                rules += text + "\n"

    instruction_data_cache = {
        "files": files,
        "rules": rules,
    }

    return instruction_data_cache


def hide_sensitive_data(text: str):
    """
    Esconde dados sensíveis de forma simples antes de enviar ao modelo.
    """
    clean_text = text
    clean_text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[email removido]", clean_text)
    clean_text = re.sub(r"\b\d{4,}\b", "[numero removido]", clean_text)
    clean_text = re.sub(r"(?i)(senha\s*[:=]?\s*)(\S+)", r"\1[removida]", clean_text)
    clean_text = re.sub(r"(?i)(token\s*[:=]?\s*)(\S+)", r"\1[removido]", clean_text)
    clean_text = re.sub(r"(?i)(cvv\s*[:=]?\s*)(\S+)", r"\1[removido]", clean_text)
    return clean_text


def is_out_of_scope(agent_id: int, question: str):
    """
    Bloqueia perguntas claramente fora do escopo do agente escolhido.
    """
    text = question.lower()

    fraud_keywords = [
        "fraude", "golpe", "pix", "phishing", "senha", "token",
        "cartão", "compra não reconhecida", "whatsapp", "invasão",
    ]
    business_keywords = [
        "maquininha", "getnet", "universia", "pluxee", "esfera",
        "netshow", "parceiro", "parceiros", "digitalização",
        "curso", "podcast", "benefício", "negócio",
    ]

    has_fraud_theme = any(keyword in text for keyword in fraud_keywords)
    has_business_theme = any(keyword in text for keyword in business_keywords)

    if agent_id == 1 and has_business_theme and not has_fraud_theme:
        return True

    if agent_id == 2 and has_fraud_theme and not has_business_theme:
        return True

    return False


def load_knowledge_data():
    """
    Lê a pasta data como conhecimento consultável do RAG.
    """
    global knowledge_data_cache

    if knowledge_data_cache is not None:
        return knowledge_data_cache

    documents = []

    data_path = os.path.join(config.get_project_root(), "data")
    if not os.path.exists(data_path):
        knowledge_data_cache = documents
        return knowledge_data_cache

    for root, _, file_names in os.walk(data_path):
        for file_name in file_names:
            file_path = os.path.join(root, file_name)
            file_items = read_knowledge_file(file_path)

            for item in file_items:
                if item["text"]:
                    documents.append(item)

    knowledge_data_cache = documents
    return knowledge_data_cache


def read_knowledge_file(file_path: str):
    """
    Lê um arquivo de conhecimento da pasta data.
    """
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        items = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                items.append(
                    {
                        "text": page_text.strip(),
                        "file_name": file_path,
                        "page": page_number,
                    }
                )

        return items

    return [
        {
            "text": open(file_path, "r", encoding="utf-8").read(),
            "file_name": file_path,
            "page": "-",
        }
    ]
    
