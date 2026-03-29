# 🤖 Assistente Inteligente com IA Generativa

## 📌 Sobre o Projeto

Este projeto é um assistente de IA que permite ao usuário tirar dúvidas de forma simples e rápida, utilizando modelos de linguagem e técnica de RAG (Retrieval-Augmented Generation).

O sistema utiliza uma base de conhecimento local para gerar respostas mais precisas e direciona o usuário para atendimento humano quando necessário.

A interação é feita via terminal, com agentes especializados por tema.

---

## 🚀 Como Iniciar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variável de ambiente

Crie um arquivo `.env`:

```env
OPENAI_API_KEY=your_api_key_here
```

### 3. Executar o projeto

```bash
python main.py
```

---

## 💬 Como Utilizar

1. Ao iniciar, escolha um agente digitando o número correspondente
2. Faça sua pergunta normalmente
3. O sistema responderá com base na base de conhecimento
4. Comandos disponíveis:

   * `voltar` → retornar ao menu de agentes
   * `sair` → encerrar o sistema

---

## 🧠 Exemplo de Perguntas

* Como posso me prevenir contra fraudes?
* Como entrar em contato com o banco?
* Como investir?
* Como me candidatar a uma vaga?

---

## ⚠️ Observação

Este projeto é um MVP desenvolvido para demonstrar o uso de IA generativa com RAG em um cenário de atendimento.
