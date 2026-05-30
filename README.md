# 🤖 Assistente Inteligente com IA Generativa

## 📌 Sobre o Projeto

Este projeto é um assistente de IA que permite ao usuário tirar dúvidas de forma simples e rápida, utilizando modelos de linguagem e técnica de RAG (Retrieval-Augmented Generation).

O sistema utiliza uma base de conhecimento local para gerar respostas mais precisas e direciona o usuário para atendimento humano quando necessário.

A interação é feita via terminal, com agentes especializados por tema.

---

## 🚀 Como Iniciar

### 0. Instalar o Python (caso ainda não tenha)

1. Acesse: https://www.python.org/downloads/
2. Baixe a versão mais recente do Python
3. Durante a instalação, marque a opção **"Add Python to PATH"**
4. Após instalar, verifique no terminal:

```bash
python --version
```

Se aparecer a versão do Python, está tudo certo :D

---

### 1. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
```

Tem o Visual Studio Code instalado? Melhor ainda! 
Vá nas extensões e use a do próprio Python.. rápida e fácil.

Ativar o ambiente:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 3. Configurar variável de ambiente

Crie um arquivo `.env` (siga `.env.example`):

```env
OPENAI_API_KEY=your_api_key_here
```

Para obter uma chave de API da OpenAI:
1. Vá em [OpenAI API Keys](https://platform.openai.com/api-keys) e crie uma nova secret
2. Copie a secret e cole no .env descrito acima
3. Lembre-se de colocar créditos de uso (cobrança em dólares americanos) em [OpenAI Billing](https://platform.openai.com/settings/organization/billing/overview) em "Add to credit ballance" - o modelo de exemplo utilizado no projeto não gasta muito!
4. Na aba "Security", como recomendação, vá em "IP allowlist" e inclua o seu IP como única permissão de uso de suas chaves OpenAI [Open AI IP allowlist](https://platform.openai.com/settings/organization/security/ip-allowlist)


---

### 4. Executar o projeto

```bash
python main.py
```

---

## 💬 Como Utilizar

1. Ao iniciar, escolha um agente digitando o número correspondente
2. Faça sua pergunta normalmente
3. O sistema responderá com base na base de conhecimento

Comandos disponíveis:

* `trocar` → retornar ao menu de agentes
* `sair` → encerrar o sistema

---

## 🧠 Exemplo de Perguntas

* Como posso me prevenir contra fraudes?
* Como entrar em contato com o banco?
* Como investir?

---

## ⚠️ Observação

Este projeto é um MVP desenvolvido para demonstrar o uso de IA generativa com RAG em um cenário de atendimento.
