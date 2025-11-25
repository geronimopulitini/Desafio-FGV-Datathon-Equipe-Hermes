# Projeto Hermes

**Simulando investidores com IA para maximizar retornos no mercado de criptoativos**  
Datathon FGV 2025

Gerônimo Pulitini · Helena Metello · Hugo Hickman · Isabelle Leal · Maurício Lima

---

## 🔎 Visão Geral

O **Hermes** investiga como **IA generativa** pode simular investidores veteranos do mercado de criptoativos para apoiar decisões de alocação em um ambiente de **alta volatilidade**, forte **assimetria de informação** e impacto de **narrativas**.

Construímos um **investidor sintético multiagente**, inspirado no estilo de decisão de **Changpeng Zhao**, fundador da Binance. A ideia é emular sua filosofia — foco em fundamentos, ciclos de mercado, comunidade e produtos com uso real — para montar e rebalancear uma **carteira de criptomoedas de 1 ano**, combinando:

- **Camada quantitativa**  
  - Previsão de retornos  
  - Modelagem de risco  
  - Simulações de Monte Carlo e métricas clássicas (Sharpe, drawdown, VaR etc.)

- **Camada qualitativa (RAG + LLM)**  
  - Notícias, relatórios e eventos de mercado  
  - Sentimento em redes sociais (por exemplo, Reddit)  
  - Narrativas de hype e contexto macroeconômico

As duas visões são integradas via **modelo Black-Litterman**, produzindo **pesos ótimos** para a carteira a partir da combinação entre opinião “do investidor simulado” e evidência quantitativa.

---

## 🧠 Arquitetura & Metodologia

O pipeline opera em **ciclos mensais** e segue cinco etapas principais:

1. **Coleta de dados**  
   - Web scraping e APIs de preços  
   - Redes sociais (por exemplo, Reddit)  
   - Notícias financeiras e eventos de mercado  
   - Indicadores macroeconômicos

2. **Geração de sinais**
   - **Expected Return Score (quantitativo)** a partir de modelos preditivos e regressões fatoriais  
   - **Conviction Score (qualitativo)** de 0 a 10, calculado via LLM + RAG com base no “clone” do investidor

3. **Seleção de ativos**
   - Universo inicial de criptomoedas  
   - Filtros eliminatórios coerentes com o perfil do investidor  
   - Hardcap de **20% por ativo** e restrições de liquidez

4. **Construção da carteira**
   - Integração dos sinais qualitativos e quantitativos no **Black-Litterman**  
   - Otimização com restrições (apenas posições compradas, sem alavancagem)  
   - Saída: vetor de pesos ótimos para a carteira

5. **Backtest**
   - Benchmark principal: **HASH11**  
   - Relato de métricas de performance e risco: retorno anualizado, volatilidade, Sharpe, alfa CAPM, VaR, hit ratio, drawdown etc.

---

## 📊 Modelos Preditivos Utilizados

Famílias de modelos empregadas na camada quantitativa:

- **Baselines**  
  - Naive  
  - Moving Average  
  - Rolling Linear

- **Séries temporais clássicas**  
  - ARIMA, SARIMA, SARIMAX  
  - ETS (Error, Trend, Seasonality)  
  - Modelos de Estado-Espaço (ex.: Kalman Local Linear Trend – LLT)

- **Machine Learning / Boosting**  
  - XGBoost  
  - LightGBM  

- **Modelos com variáveis exógenas / deep learning**  
  - ExogLSTM  
  - Seq2Seq  

- **Modelos distribucionais**  
  - DistModel → estima **distribuições completas de retorno**, não apenas ponto médio

---

## 🧱 Dados & Fontes

O Hermes integra diferentes blocos de dados:

- **Mercado de cripto**
  - Preços, retornos, volume e volatilidade (via APIs de mercado de cripto)
- **Narrativas e sentimento**
  - Postagens em redes sociais (por exemplo, API do Reddit)
  - Notícias gerais e financeiras
- **Macroeconomia**
  - Indicadores macroeconômicos utilizados como exógenas (por exemplo, bases no estilo FRED)

---

## ⚙️ Instalação e Ambiente

> 💡 **Importante:** para rodar o projeto é **obrigatório** configurar as chaves de API e demais credenciais via variáveis de ambiente.  
> Os nomes das variáveis e detalhes de configuração estão descritos no arquivo `exemplo.env`.

1. **Clone o repositório**

   git clone https://github.com/.../hermes.git
   cd hermes

2. **Crie um ambiente virtual (opcional, mas recomendado)**

   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate   # Windows

3. **Instale as dependências**

   pip install -r requirements.txt

4. **Configure as variáveis de ambiente**

   - Copie o arquivo de exemplo:

     cp exemplo.env .env

   - Edite o `.env` com suas chaves de API, por exemplo:
     - API de redes sociais (ex.: Reddit)  
     - Provedor de LLM (ex.: Gemini / outro)  

   Sem esse passo, os módulos de **coleta de dados**, **RAG** e **modelagem** não funcionarão corretamente.

5. **Execução**

   - Consulte os scripts na pasta `src/` (ou equivalente) para:
     - Rodar a coleta de dados  
     - Treinar os modelos  
     - Executar o backtest e gerar os relatórios da carteira  

---

## 👥 Equipe

- **Gerônimo Pulitini** – Ciências Econômicas, PUC-Rio  
- **Helena Metello** – Engenharia de Produção, PUC-Rio  
- **Hugo Hickman** – Engenharia de Produção, PUC-Rio  
- **Isabelle Leal** – Estudos de Mídia, PUC-Rio  
- **Maurício Lima** – Engenharia de Produção, PUC-Rio  

---

## ⚖️ Aviso Legal

Este projeto tem **fins exclusivamente acadêmicos e de pesquisa**.  
Nenhuma informação presente aqui constitui recomendação de investimento, indicação de compra ou venda de ativos, nem oferta de produtos financeiros.

---

## ⭐ Apoie o Repositório

Se este projeto foi útil ou interessante para você, considere deixar uma **⭐ no GitHub** e compartilhar com outras pessoas interessadas em **IA aplicada a criptoativos**.
