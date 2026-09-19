Cenário Escolhido

Cenário A: Conciliação bancária diária feita a partir do download do extrato .csv e comparação das linhas com as baixas do sistema ERP via regras fixas de CNPJ e valor.

1. Nome do Processo

Conciliação Bancária Diária

2. É viável para RPA? (Sim / Não)

Sim.

3. Justificativa baseada nos 4 critérios essenciais
Critério	Análise
Repetitividade	O processo é executado todos os dias úteis, sempre seguindo a mesma sequência de passos (baixar extrato, comparar, classificar, registrar). Alta repetitividade favorece a automação.
Regras de Negócio	A decisão de conciliar ou não um lançamento é 100% objetiva: basta verificar se existe, no ERP, um registro com o mesmo CNPJ e mesmo valor do extrato. Não há julgamento subjetivo envolvido.
Tipo de Dados	Os dados são estruturados: o extrato é um arquivo .csv com colunas fixas (data, CNPJ, valor, histórico), e o ERP também expõe os lançamentos em formato tabular/consultável.
Volume	O processo trata entre 200 e 500 linhas por dia, um volume relevante o suficiente para justificar o investimento em automação e gerar ganho real de tempo.

Conclusão: o processo atende integralmente aos 4 critérios (repetitividade, regras claras, dados estruturados e volume relevante), sendo um caso clássico de alta elegibilidade para RPA.

4. Mapeamento Passo a Passo das Ações do Robô
Iniciar execução — robô é disparado automaticamente após a disponibilização do extrato bancário do dia (gatilho agendado, ex.: todo dia útil às 7h).
Baixar/acessar o extrato — robô acessa o internet banking (ou pasta compartilhada) e baixa o arquivo extrato_banco.csv.
Ler dados do ERP — robô consulta o sistema ERP (via tela, API ou exportação) e extrai a lista de baixas registradas.
Carregar e padronizar os dados — robô lê o .csv e a base do ERP, padronizando formato de CNPJ e valor (remoção de máscaras, ajuste de casas decimais).
Comparar registros — para cada linha do extrato, robô busca no ERP um lançamento com mesmo CNPJ e mesmo valor.
Classificar o lançamento:
Se encontrar correspondência exata → marcar como conciliado.
Se não encontrar → mover para lista de pendências.
Se encontrar mais de uma correspondência possível → sinalizar para revisão humana.
Gerar relatório — robô consolida os resultados em uma planilha/relatório de conciliação (itens conciliados x pendentes).
Notificar responsáveis — robô envia e-mail/mensagem ao time financeiro com o resumo da execução e o relatório em anexo.
Registrar log de execução — robô grava log com horário de início/fim, quantidade de itens processados e eventuais erros.
Tratar exceções de sistema — caso o extrato não esteja disponível ou o ERP esteja inacessível, robô interrompe a execução e notifica a equipe de suporte.