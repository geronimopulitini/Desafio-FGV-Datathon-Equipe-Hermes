Projeto Hermes

Simulando Investidores com IA para Maximizar Retornos no Mercado de Criptoativos

Projeto desenvolvido para o Datathon FGV 2025 por
Gerônimo Pulitini · Helena Metello · Hugo Hickman · Isabelle Leal · Maurício Lima

Visão Geral

O Projeto Hermes investiga como inteligência artificial generativa pode simular investidores veteranos do mercado de criptomoedas para otimizar decisões de investimento em um ambiente de alta volatilidade.

Construímos um investidor sintético multiagente, modelado a partir do estilo de decisão de Changpeng Zhao (CZ) — fundador da Binance — para montar uma carteira de cripto por 1 ano, combinando:

Modelagem quantitativa: previsões de retorno, risco e simulações de Monte Carlo

Modelagem qualitativa: narrativas, notícias, Reddit e eventos de mercado via RAG

Modelo Black-Litterman para conciliar ambas as visões em pesos ótimos


relatório hermes

Cada agente opera de forma independente e consulta uma camada de RAG (Retrieval-Augmented Generation) para acessar o conhecimento filtrado sobre o investidor simulado.

🔬 Metodologia

O pipeline da estratégia opera em ciclos mensais e contém cinco etapas principais:

Etapa	Descrição
1) Coleta de dados	Web scraping, APIs de preços, redes sociais, notícias e relatórios
2) Geração de sinais	Conviction Score (qualitativo) + Expected Return Score (quantitativo)
3) Seleção de ativos	Filtros eliminatórios baseados no investidor + hardcap 20%
4) Black-Litterman	Integração qualitativa + quantitativa com otimização restrita
5) Backtest	Benchmark HASH11, métricas de performance e risco
Modelos Preditivos Utilizados

Naive, Moving Average e Rolling Linear

ARIMA, SARIMA, SARIMAX

ETS

Kalman LLT

XGBoost / LightGBM

ExogLSTM / Seq2Seq

DistModel → distribuições completas de retorno


👥 Equipe
Gerônimo Pulitini	- Ciências Econômicas – PUC-Rio
Helena Metello	- Engenharia de Produção – PUC-Rio
Hugo Hickman	- Engenharia de Produção – PUC-Rio
Isabelle Leal	- Estudos de Mídia – PUC-Rio
Maurício Lima	- Engenharia de Produção – PUC-Rio

⚖️ Aviso Legal

O projeto possui objetivos acadêmicos e de pesquisa.
O estudo não constitui recomendação de investimento.

⭐ Apoie o Repositório

Se você gostou do projeto considere deixar uma ⭐ no GitHub.
