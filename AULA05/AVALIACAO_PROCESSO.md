Cenário: A

1. Nome do Processo
Conciliação bancária diária (extrato CSV x baixas ERP)
2. É viável para RPA? (Sim / Não)
Sim
3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).
*Repetitividade: esse processo é realizado todos os dias, sempre com a mesma logica de passos sem variação no fluxo (baixar extrato e comparação das linhas com as baixas do sistema ERP)
*Regras de negócio: o processo tem regras claras e objetivas, se o CNPJ, valor e data do extrato bate com a baixa do sistema considera-se conciliada, caso contratio não concilia. 
*Tipo de dados: dados bem estruturados e fixos com colunas: CNPJ, valor, data
*Volume: o processo compõe um volume grande de linhas do movimento financeiro gerado pelo extrato, se feito manualmente leva-se horas e sujeuti a erros de comparação. O robô faz isso em segundos de maneira precisa e padronizada.
4. Mapeamento Passo a Passo das Ações do Robô

1. inicio em horario especifico (agendado)
2. ler csv
3. ler baixas no ERP
4. busca e comparação csv x ERP
5. Se a correspondência for encontrada, marcar "Conciliado", se a correspondência não for encontrada, marcar como "Divergência", se houver mais de uma corrspondência marcar como "Duplicada" para análise.
6. Gerar relatório contendo as conciliações, divergências e duplicações.
7. Enviar relatório ao time financeiro
8. Gravar log da execução
9. Finalizar robô
