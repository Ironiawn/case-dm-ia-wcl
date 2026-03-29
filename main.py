from engine import orchestrator
from engine.agent import tag_sessao_encerrada
from termcolor import colored
from datetime import datetime
import os


def select_agent():
    """
    Pede ao usuário um agente válido.
    """
    while True:
        agent_id = input("Selecione um agente (1 - Anti-Fraude, 2 - Soluções): ")

        try:
            if agent_id in ["1", "2"]:
                return int(agent_id)
        except:
            pass

        print("Agente inválido. Escolha 1 ou 2.")


def write_audit_log(question: str, audit_items: list[dict]):
    """
    Grava a auditoria dos chunks usados na resposta em um arquivo de log.
    """
    if not audit_items:
        return

    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "rag_audit.log")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{current_time}] pergunta: {question}\n")

        for item in audit_items:
            score = round(item["score"], 4)
            page = item["page"]
            file_name = item["file_name"]
            chunk_id = item["chunk_id"]
            log_file.write(
                f"arquivo: {file_name} | pagina: {page} | chunk_id: {chunk_id} | score: {score}\n"
            )

        log_file.write("\n")


agent_id = select_agent()
history_items = []
history_limit = 6

while True:
    question = input(colored("Pergunta: (digite sair para sair e trocar para mudar o agente) ", "cyan"))
    command = question.strip().lower()

    if command == "sair":
        print(colored("Sessão encerrada.", "yellow"))
        break

    if command == "trocar":
        agent_id = select_agent()
        continue

    session_history = "\n\n".join(history_items)
    result = orchestrator.orchestrate(agent_id, question, session_history)
    answer = result["answer"]
    should_end_session = tag_sessao_encerrada in answer
    clean_answer = answer.replace(tag_sessao_encerrada, "").strip()

    print(colored("Agente:", "green"), colored(clean_answer, "white"))
    write_audit_log(question, result["audit"])

    history_items.append(f"Usuário: {question}\nAgente: {clean_answer}")

    if len(history_items) > history_limit:
        history_items = history_items[-history_limit:]

    if should_end_session:
        print(colored("Sessão encerrada.", "red"))
        break
