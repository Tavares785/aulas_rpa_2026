Cenário: Cenário A

1. Nome do Processo
Conciliação Bancária Diária

2. É viável para RPA? (Sim / Não)
Sim

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume):
- Repetitividade: Processo realizado diariamente seguindo uma sequência padronizada de passos.
- Regras de Negócio: Regras claras e bem definidas baseadas na comparação do CNPJ e do valor entre o extrato e o ERP.
- Tipo de Dados: Dados estruturados provenientes do download do arquivo .csv e dos registros do sistema ERP.
- Volume: Execução diária de comparações linha a linha, garantindo maior ganho de produtividade e redução de erros manuais.

4. Mapeamento Passo a Passo das Ações do Robô
1. Acessar o sistema bancário ou diretório local e realizar o download do arquivo de extrato em formato .csv.
2. Ler e processar as linhas do arquivo .csv extraindo CNPJ e valor.
3. Acessar o sistema ERP e consultar as baixas pendentes correspondentes aos CNPJs e valores identificados.
4. Comparar as informações entre o extrato e o ERP seguindo as regras fixas de correspondência.
5. Executar a baixa automática no ERP para os registros correspondentes.
6. Gerar um relatório final ou log informando as conciliações efetuadas e marcando as exceções/divergências para análise humana.



