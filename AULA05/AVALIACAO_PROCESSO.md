# Ficha de Avaliação de RPA

**Cenário:** B - Triagem de solicitações de reembolso de despesas médicas

## 1. Nome do Processo

Triagem e autorização de reembolsos de despesas médicas com base na análise de empatia e no histórico emocional do paciente.

## 2. É viável para RPA?

**Não.**

O processo não é adequado para uma decisão automatizada por RPA, pois depende de interpretação subjetiva e de julgamento humano sobre o estado emocional do paciente. Um robô de RPA pode executar tarefas administrativas de apoio, mas não deve decidir sozinho se o reembolso será autorizado com base nesses critérios.

## 3. Justificativa pelos quatro critérios essenciais

| Critério | Avaliação |
|---|---|
| **Repetitividade** | A entrada e o cadastro das solicitações podem ser repetitivos, mas a análise necessária para autorizar cada caso varia de acordo com a situação do paciente. |
| **Regras de negócio** | **Não atende.** “Empatia” e “histórico emocional” são critérios subjetivos, difíceis de transformar em regras claras, consistentes e auditáveis. |
| **Tipo de dados** | **Não atende completamente.** Os documentos da despesa podem ser estruturados, porém as informações emocionais são sensíveis, interpretativas e podem estar em textos livres ou avaliações humanas. |
| **Volume** | Pode haver alto volume de solicitações, o que favorece a automação de tarefas operacionais, mas volume por si só não compensa a ausência de regras objetivas para a decisão. |

## 4. Mapeamento passo a passo das ações do robô

Como o processo completo não é viável, o robô deve limitar-se às atividades administrativas e encaminhar a decisão para um analista autorizado:

1. Acessar o portal ou a caixa de entrada onde as solicitações são recebidas.
2. Registrar cada solicitação em uma fila, atribuindo um identificador único.
3. Extrair dados objetivos, como nome ou identificador do beneficiário, data, valor e número do comprovante.
4. Conferir se os campos obrigatórios e os anexos foram preenchidos, sem interpretar o estado emocional do paciente.
5. Identificar solicitações incompletas e enviar uma mensagem padronizada solicitando os documentos faltantes.
6. Encaminhar as solicitações completas para um profissional responsável pela análise humana.
7. Registrar no sistema a decisão e a justificativa fornecidas pelo profissional.
8. Atualizar o solicitante sobre o resultado conforme a decisão registrada.
9. Gerar um relatório de volume, pendências e tempo de atendimento para acompanhamento.

**Conclusão:** o RPA pode apoiar o recebimento, a conferência documental, o encaminhamento e os registros do processo, mas a autorização do reembolso não deve ser automatizada com base em empatia ou histórico emocional.