# Lab 08: Web Scraping e Interação com Elementos via Selenium

## 🎯 Objetivos de Aprendizagem
- Configurar e instanciar o Selenium WebDriver (`webdriver.Chrome`)
- Mapear elementos HTML usando diferentes seletores (`By.TAG_NAME`, `By.XPATH`, `By.CSS_SELECTOR`)
- Implementar esperas (`implicitly_wait` ou `WebDriverWait`) para lidar com conteúdo carregado via JavaScript
- Coletar dados de uma página real (*web scraping*) e organizá-los em uma estrutura de dados

## 💼 Desafio de Mercado
Ao contrário da automação Desktop (baseada em imagem ou coordenadas estáticas), a automação Web inspeciona a árvore DOM do navegador. Isso garante alta performance e independe de resolução de tela. Muitos sites modernos montam o conteúdo dinamicamente com JavaScript, por isso o Selenium (navegador real) consegue "enxergar" dados que o `requests` sozinho não veria.

---

## 📝 Enunciado (Aluno)

1. Instale a biblioteca `selenium` (o Selenium 4.6+ já baixa o driver do Chrome automaticamente)
2. Crie o script `bot_products_harry.py`
3. O bot deve abrir o navegador Chrome no site oficial: `https://www.harrypotter.com/pt/login`
5. Navegue até https://harrypottershop.com/collections/gifts/Under-$10
6. Para cada produto, extraia o **Titulo** e a **Preço** e guarde em uma lista de dicionários, ex.: `{"titulo": ..., "Preço": ...}`
7. Ao final, exiba no terminal todos os produtos encontrados (Titulo + Preço) e a quantidade total coletada

---


## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab08/SEU_RA` (ex: `lab08/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab08/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab08: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab08/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab08] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
