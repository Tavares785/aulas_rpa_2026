# Ficha de Avaliação de RPA

## Cenário
Cenário B – Triagem de solicitações de reembolso de despesas médicas.

## 1. Nome do Processo
Triagem de Solicitações de Reembolso Médico.

## 2. É viável para RPA?
Não.

## 3. Justificativa baseada nos 4 critérios essenciais

### Repetitividade
A triagem de solicitações de reembolso pode acontecer com bastante frequência,
já que diferentes pedidos precisam ser analisados ao longo do tempo. Apesar
disso, cada solicitação pode envolver uma situação diferente, principalmente
porque a decisão não depende apenas de informações objetivas presentes no
pedido.

### Regras de Negócio
Esse é o principal problema para a utilização de RPA nesse processo. A decisão
de autorizar o reembolso é baseada na análise de empatia e no histórico
emocional do paciente. Esses critérios são subjetivos e não possuem regras
claras que possam ser facilmente transformadas em condições que um robô
consiga seguir.

Diferente de uma comparação de valores ou documentos, não existe uma regra
simples que determine quando uma situação deve ou não ser considerada
adequada para autorização. Por isso, diferentes casos podem exigir
interpretação e julgamento humano.

### Tipo de Dados
Parte das informações utilizadas durante a análise pode estar estruturada,
como dados cadastrais, valores e informações sobre solicitações anteriores.
Porém, informações relacionadas ao histórico emocional e à situação do
paciente podem estar presentes em textos, observações ou outros dados que
não seguem necessariamente um padrão.

Isso dificulta a utilização de um RPA tradicional, que funciona melhor quando
os dados possuem uma estrutura previsível e podem ser tratados através de
regras previamente definidas.

### Volume
Mesmo que exista um grande volume de solicitações, isso não significa que o
processo inteiro seja adequado para automação. O volume poderia justificar a
automatização de algumas etapas mais simples, como organizar documentos,
consultar informações ou cadastrar solicitações.

Porém, a decisão final de autorizar ou não o reembolso continuaria dependendo
de uma análise humana, devido aos critérios subjetivos utilizados no processo.

## 4. Mapeamento Passo a Passo das Ações do Robô

Como o processo completo não é adequado para RPA, o robô poderia ser utilizado
apenas como apoio nas etapas que possuem regras mais claras.

1. Receber a solicitação de reembolso.
2. Identificar os dados básicos da solicitação.
3. Verificar se os documentos necessários foram enviados.
4. Consultar informações cadastrais e solicitações anteriores.
5. Organizar os dados encontrados para facilitar a análise.
6. Encaminhar a solicitação para o responsável pela avaliação.
7. O responsável realiza a análise dos critérios subjetivos, como o histórico
   emocional e a situação apresentada pelo paciente.
8. Após a decisão humana, o robô pode registrar o resultado no sistema.
9. Finalizar o processo.
