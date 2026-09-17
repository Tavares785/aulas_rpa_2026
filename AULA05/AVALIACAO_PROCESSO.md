# Avaliação de Viabilidade de RPA - Cenário A

### 1. Nome do Processo
Conciliação Bancária Diária via ERP

### 2. É viável para RPA?
**SIM**

### 3. Justificativa baseada nos 4 critérios essenciais
* **Repetitividade:** Alta. O processo é executado de forma cíclica e idêntica todos os dias úteis, exigindo que o mesmo conjunto de etapas lógicas seja aplicado para cada transação financeira encontrada.
* **Regras de Negócio:** Totalmente baseadas em regras claras. A validação não exige julgamento subjetivo ou interpretação humana; o cruzamento de dados segue a lógica matemática binária e estrita de correspondência exata entre chaves fixas (CNPJ e Valor).
* **Tipo de Dados:** Altamente Estruturados. Os dados de entrada estão organizados em colunas e linhas definidas no formato padrão `.csv` (extrato bancário) e em campos sistêmicos mapeáveis dentro do banco de dados/telas do ERP.
* **Volume:** Alto. Por ser uma rotina diária corporativa que engloba todas as movimentações financeiras da empresa, apresenta um fluxo massivo de dados transacionais, tornando a execução manual propensa a erros de digitação e exaustão.

### 4. Mapeamento Passo a Passo das Ações do Robô
1. **Inicialização:** O robô inicia a execução, acessa de forma segura o gerenciador de credenciais e obtém os dados de login para o Internet Banking e o sistema ERP.
2. **Extração do Extrato:** O robô abre o navegador web corporativo, acessa o portal do Internet Banking, realiza a autenticação, navega até a área financeira e efetua o download do arquivo de extrato diário em formato `.csv`.
3. **Leitura de Dados:** O robô lê o arquivo `.csv` baixado e armazena os dados em uma tabela em memória (Data Table) para processamento.
4. **Autenticação no ERP:** O robô abre a interface do sistema ERP corporativo e realiza o login na plataforma.
5. **Loop de Processamento:** Para cada linha contida no extrato bancário `.csv`, o robô executa as seguintes subetapas:
   - Extrai as variáveis `CNPJ` e `Valor` da linha atual.
   - Navega até o módulo de conciliação financeira do ERP.
   - Insere as variáveis nos filtros de busca do sistema para localizar a baixa correspondente.
   - **Fluxo de Sucesso (Regra de Negócio):** Se o ERP localizar um lançamento com o mesmo CNPJ e Valor exato, o robô clica em "Confirmar/Efetuar Baixa".
   - **Fluxo de Exceção (Regra de Negócio):** Se os valores divergirem ou o CNPJ não for localizado no sistema, o robô isola o registro em uma lista de exceções e grava o erro no arquivo de log.
6. **Finalização:** Após processar todas as linhas do arquivo, o robô fecha as sessões do navegador e do ERP, gera um relatório consolidado com o status da conciliação e envia um e-mail de notificação para a equipe financeira com a lista de divergências encontradas.
