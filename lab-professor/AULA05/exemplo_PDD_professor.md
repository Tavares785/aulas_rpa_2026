# Ficha de Avaliacao de RPA (PDD simplificado)


## 1. Identificacao do Processo
- **Nome:** Baixa automatica de titulos a pagar com conferencia de notas fiscais de entrada
- **Area:** Financeiro / Contas a Pagar
- **Frequencia:** Diaria (lotes ao longo do dia util)
- **Volume:** ~450 titulos por dia

## 2. Criterios de Elegibilidade (checklist)
| Criterio | Atende? | Observacao |
|---|---|---|
| Regras claras e objetivas | ✅ | Confere numero da NF, fornecedor e valor contra o titulo, sem julgamento subjetivo |
| Dados estruturados | ✅ | Arquivo de retorno do ERP com colunas fixas (NF, fornecedor, vencimento, valor) |
| Alto volume / repetitivo | ✅ | Centenas de baixas identicas por dia |
| Baixa taxa de excecao | ✅ | Divergencias de valor caem em fila de revisao manual |
| Sistema estavel (nao muda a toda hora) | ✅ | Tela de lancamento do ERP padronizada |

**Veredito:** ALTAMENTE ELEGIVEL para RPA.

## 3. Contra-exemplo
Um processo de triagem de curriculos que seleciona candidatos "por
afinidade cultural subjetiva com o time" NAO e elegivel: a decisao
depende de percepcao humana, as regras nao sao deterministicas e o
resultado nao e auditavel nem reproduzivel.

## 4. Beneficios Esperados
- Reducao de ~5h de trabalho manual/dia na equipe de pagamentos
- Eliminacao de divergencias de valor nao percebidas na conferencia
- Trilha de auditoria automatica (logs) para cada baixa realizada

## Dica de conducao da aula
Peca para cada aluno classificar 3 processos do dia a dia deles como
"elegivel" ou "nao elegivel" e justificar usando o checklist acima.
