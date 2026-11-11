# Lab 10: Extração de Dados da Web em Escala com BeautifulSoup

## 🎯 Objetivos de Aprendizagem
- Fazer requisições HTTP seguras usando a biblioteca `requests`.
- Parsear a árvore DOM do HTML com a classe `BeautifulSoup`.
- Navegar e extrair dados via métodos `find()`, `find_all()` e seletores CSS (`select`).
- Aplicar princípios éticos de Web Scraping e tratamento do arquivo `robots.txt`.

## 💼 Desafio de Mercado
Diferente do Selenium (que simula um navegador real e consome muita memória/CPU), o `BeautifulSoup` combinado com `requests` realiza raspagem de dados extremamente veloz em sites estáticos ou server-side rendered, sendo a ferramenta perfeita para **monitoramento de preços de concorrentes** no e-commerce. Neste laboratório você vai raspar um catálogo de produtos de uma loja real (loja oficial do Harry Potter, construída em Shopify), extraindo nome e preço de cada item.

---

## 📝 Enunciado (Aluno)

1. Instale as bibliotecas `requests` e `beautifulsoup4`.
2. Crie o script `scraper_loja.py`.
3. O bot deve fazer uma requisição HTTP para a página de catálogo da casa Grifinória:
   `https://harrypottershop.co.uk/collections/gryffindor`
4. Envie um cabeçalho `User-Agent` de navegador real na requisição (boa prática para não ser bloqueado) e valide se a resposta do servidor foi `200 OK`.
5. Utilize o `BeautifulSoup` com o parser `'html.parser'` para converter o conteúdo.
6. Localize todos os **cards de produto** da listagem e, para cada um, extraia:
   - **Nome do produto** (ex: `Gryffindor Metal Crest Journal`).
   - **Preço** (ex: `£18.95`).
7. Limpe o texto extraído removendo espaços e quebras de linha desnecessárias (`.strip()` / normalização de espaços).
8. Exiba os 5 primeiros produtos no terminal e salve a lista completa em um arquivo CSV (`produtos_gryffindor.csv`) com as colunas `nome` e `preco`.

> 💡 **Dica:** a loja é feita em Shopify. Os cards de produto costumam usar a classe CSS `.card` e o título fica em um elemento com a classe `.card__heading` (geralmente dentro de um `<a>`). O preço aparece em elementos com a classe `.price-item` (o preço efetivo é o `.price-item--sale` quando o produto está em promoção, ou o `.price-item--regular`). Inspecione o HTML com o DevTools (F12) do navegador para confirmar os seletores antes de codar.

---



## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab10/SEU_RA` (ex: `lab10/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab10/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab10: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab10/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab10] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
