import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_project_root():
    """
    Obtém o diretório raiz do projeto
    """
    return BASE_DIR