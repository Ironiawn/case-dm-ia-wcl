Documento explicativo de motivos de cada escolha do projeto.



**Geração e Embeddings**



A solução utiliza a API da OpenAI com os modelos gpt-5-nano para geração de respostas e text-embedding-3-small para embeddings.

A escolha por APIs em vez de modelos locais foi feita para garantir portabilidade e execução em qualquer máquina, evitando dependência de hardware.



**GPT-5-Nano**

1 -> Menor custo possível para processamento e respostas

2 -> Modelo pequeno e de rápida resposta

3 -> Adequado para perguntas simples e base de conhecimento limitada



**text-embedding-3-small**

1 -> Base de dados pequena, não requer embedding grande para contextos

2 -> Seguindo a lógica de escolha do GPT-5-Nano: custos e velocidade de geração de retornos

3 -> Menor custo computacional



**Uso de RAG (Retrieval-Augmented Generation)**

Utilização de base de dados locais melhora a precisão das respostas, reduz o risco de alucinações, não requer re-treinamento (fine-tuning) de modelos e permite respostas baseadas em dados confiáveis.



Como o projeto foi criado na intenção de modularidade e fácil manutenção, a possibilidade de aumentar bases e agentes também se torna rápida e fácil.



**Lado negativo**

**RAG ->** Dados precisam ter uma qualidade verificada | Necessidade de chunkings e embeddings

**API ->** Pode ser necessário aprovação de segurança da informação em ambientes corporativos | Dependência de serviços externos | Custos variáveis (caso não haja controle adequado do uso) | Necessidade de controle de dados enviados para evitar exposição de informações sensíveis





**Considerações Gerais**

O projeto foi desenvolvido com foco em simplicidade, modularidade e fácil manutenção, permitindo evolução incremental da solução.

