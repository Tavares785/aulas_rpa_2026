Cenário: 
    **Cenário A:** Conciliação bancária diária feita a partir do download do extrato `.csv` e comparação das linhas com as baixas do sistema ERP via regras fixas de CNPJ e valor.

1. Nome do Processo:
    Conciliação Bancária Diária.

2. É viável para RPA? (Sim / Não) 
    Sim.

3. Justificativa baseada nos 4 critérios essenciais (Repetitividade, Regras de Negócio, Tipo de Dados, Volume).
    É uma tarefa repetitiva pois trata-se basicamente de comparar valores entre o csv e o sistema ERP, verificando se eles batem. Possui uma passo a passo lógico e simples, não há subjetividade neste processo, os valores são comparados e há uma verificação lógica para ver se as entradas/saídas do csv são as mesmas no ERP. São dados bem estruturados, relativamente simples CNPJ + valor. A movimentação bancária de uma empresa depende muito do seu tamanho, portanto o volume depende muito deste fator, mas mesmo assim, é uma quantidade considerável de dados a serem comparados tornando a automatização do processo viável.

4. Mapeamento Passo a Passo das Ações do Robô
    Baixar o extrato .csv
    Acessar as informarção de movimentação bancária diária no ERP
    Comparar os dados, CNPJ + Valor + Tipo de movimentação (entrada ou saída)
    Verificar se CNPJ foi encontrado -> Retornar resultado
    Verificar se os valores estão corretos -> Retornar resultado
    Verificar se o tipo de transação está correta -> retornar resultado
    Fazer o mesmo processo para toda a lista do .csv
