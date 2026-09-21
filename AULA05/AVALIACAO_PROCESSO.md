Cenário:

1. Nome do Processo
    R: Cenário B - Triagem de solicitações de reembolso de despesas médicas onde a decisão de autorizar é baseada na "análise de empatia e histórico emocional do paciente".

2. É viável para RPA? (Sim / Não)
    R: Não.

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).
    R: Se caso no cenário fosse realizado apenas a parte de "Triagem de solicitações de reembolso de despesas médicas", seria possível a criação de um RPA já que contém apenas informações de pagamentos onde o valor pago que já está armazenado seria realizado o reembolso desse mesmo valor e ser um processo repetitivo. Porém, foi informado que a decisão de autorização, se será feito o reembolso ou não, é baseada em "análise de empatia e histórico emocional do paciente", onde um sistema de RPA não consegue identificar essa informações, por cada pessoa ter um caso diferente e também o volume de pedidos pode não ser uma quantidade tão grande para valer a pena o investimento do sistema de RPA.

4. Mapeamento Passo a Passo das Ações do Robô
    R:  1. O robô pega as informações da solicitação de reembolso pelo meio onde foi realizado a solicitação.
        2. O robô extrai dados essênciais, como nome, CPF, motivo, número de atendimento e valor.
        3. Ele cria um documento com todas essas informações e cria um resumo do histórico desse paciente.
        4. Esse documento é encaminhado para uma fila onde médicos ou responsáveis, podem validar se essa situação de reembolso será aceita ou não.