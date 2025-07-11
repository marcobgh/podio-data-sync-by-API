# Podio Data Sync

Automação de atualização cadastral integrada ao Podio, com consulta em tempo real à base da Receita Federal.

## ✨ Sobre o Projeto

Esta aplicação foi desenvolvida para automatizar a verificação e atualização de dados cadastrais de clientes. Ao receber um Webhook do Podio (criação ou atualização de item), o sistema:

- Captura o CNPJ do cliente.
- Consulta os dados atualizados na Receita Federal via API pública.
- Compara os dados recebidos com os armazenados no Podio.
- Gera um resumo das divergências encontradas.
- Atualiza automaticamente o cadastro no Podio com os dados corretos.
- Preenche um campo de status com "Atualizado" ou "Desatualizado".

## ⚙️ Funcionalidades

- Integração via Webhooks com o Podio.
- Consulta automática a CNPJ com API pública.
- Comparação de objetos orientada a campos.
- Geração de logs legíveis com as divergências encontradas.
- Atualização automática do cadastro com dados consistentes.
- Verificação periódica opcional para manter base sincronizada.

## 🧱 Tecnologias Utilizadas

- Python (ou JavaScript / Java / Node.js, dependendo do seu stack)
- Webhooks (Podio)
- API ReceitaWS (ou outra pública)
- HTTP Requests
- Programação Orientada a Objetos (POO)

## 🚀 Como Usar

> Em breve: instruções de instalação, execução e exemplos.

## 📌 Observações

Este projeto foi desenvolvido inicialmente para uso interno em uma cooperativa de crédito, com foco na otimização de processos, redução de erros manuais e melhoria na confiabilidade dos dados.

---

📥 Contribuições, sugestões ou dúvidas? Fique à vontade para abrir uma issue.
