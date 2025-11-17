HOW TO RUN (Windows / PowerShell) — Atualizado

Pré-requisitos
- Python 3.10+ no PATH
- PowerShell
- Internet para instalar dependências e (opcional) coletar dados reais

Estrutura (onde executar)
- Orquestrador (pipeline completo): `Hydra\Hermes`
- CLI Hydra v2 (coleta/RAG/sumários): `Hydra\` (raiz do repo)

Modo de dados e modo estrito
- Padrão: `run_pipeline.py` usa `--data-source hydra` e `--qual-source hydra`. Use `--engine full` para forecasts reais; `--engine synthetic` agora é apenas para desenvolvimento/teste.
- Sintético (dev/teste): informe explicitamente `--engine synthetic --data-source synthetic --qual-source synthetic`.
- Estrito (produção): use `--strict-real-data` ou `HYDRA_STRICT_REAL_DATA=1`. Qualquer tentativa de fallback gera erro e nenhum relatório é emitido.
- Artefatos `forecast.json` e `portfolio.json`, além dos payloads do relatório, trazem `data_mode` (`real`, `mixed` ou `synthetic`).
- Exemplos:
  - Real (padrão): `python orchestrator/run_pipeline.py --ticker PETR4.SA --engine full --outdir artifacts --verbose`
  - Estrito: `HYDRA_STRICT_REAL_DATA=1 python orchestrator/run_pipeline.py --ticker PETR4.SA --engine full --data-source hydra --qual-source hydra --outdir artifacts --verbose`
  - Sintético: `python orchestrator/run_pipeline.py --ticker PETR4.SA --engine synthetic --data-source synthetic --qual-source synthetic --outdir artifacts --verbose`

0) Observação importante (erro comum)
- Se você criou o venv na RAIZ (`Hydra\`), tudo bem. Mas SEMPRE rode `pip install -r requirements.txt` dentro de `Hydra\Hermes` (faça `cd Hermes` antes). O arquivo `requirements.txt` não existe na raiz.

1) Preparar ambiente (Hermes)
- Abra PowerShell na pasta: `Hydra\Hermes`
- Crie e ative venv (recomendado criar aqui dentro):
  - `python -m venv .venv`
  - `. .\.venv\Scripts\Activate.ps1`
- Instale dependências e registre os pacotes locais:
  - `pip install -r requirements.txt`
  - `pip install -e .`

2) Configurar variáveis (.env)
- `Hermes/.env` (opcional, recomendado): copie de `Hermes/.env.sample` e preencha o que tiver:
  - `GOOGLE_API_KEY=...`
  - `CRYPTOCOMPARE_API_KEY=...`
  - `REDDIT_CLIENT_ID=...`, `REDDIT_CLIENT_SECRET=...`, `REDDIT_USER_AGENT=...`
  - `SEC_USER_AGENT=SeuNome/SeuEmail`
- `Hydra/.env`: use `.env.example` como base. Sem chaves, o pipeline usa fallbacks (logará avisos).

3) Executar (sintético/offline)
- Em `Hydra\Hermes` (venv ativo):
  - `python orchestrator\run_pipeline.py --ticker PETR4.SA --engine synthetic --data-source synthetic --qual-source synthetic --outdir artifacts --verbose`
- Saídas em `Hermes\artifacts\YYYY-MM-DD\`:
  - `report.pdf`, `johnson_daily.csv`, `forecast.json`, `portfolio.json`

4) Executar com Hydra (dados reais)
- Opcional (forçar apenas fontes online):
  - `$env:HYDRA_IGNORE_CSV="1"; $env:HYDRA_IGNORE_CACHE="1"`
- Rodar:
  - `python orchestrator\run_pipeline.py --ticker PETR4.SA --engine full --data-source hydra --qual-source hydra --outdir artifacts --verbose`
  - `python orchestrator\run_pipeline.py --ticker PETR4.SA --engine full --data-source hydra --qual-source hydra --outdir artifacts --strict-real-data --verbose` (estrito)
- Full (com forecast pronto):
  - `python orchestrator\run_pipeline.py --ticker PETR4.SA --engine full --forecast-path C:\caminho\forecast.json --data-source hydra --qual-source hydra --outdir artifacts --verbose`

5) Rodar 20 tickers (lote)
- Liste seus tickers (exemplo):
  - `$tickers = @('PETR4.SA','VALE3.SA','ITUB4.SA','ABEV3.SA','B3SA3.SA','BBAS3.SA','WEGE3.SA','LREN3.SA','RAIL3.SA','PRIO3.SA','JBSS3.SA','SUZB3.SA','GGBR4.SA','UGPA3.SA','EQTL3.SA','TAEE11.SA','RAIZ4.SA','CMIG4.SA','BBSE3.SA','RENT3.SA')`

- Sintético (offline):
```
foreach ($t in $tickers) {
  Write-Host "Rodando $t (synthetic)..."
  python orchestrator\run_pipeline.py --ticker $t --engine synthetic --data-source synthetic --qual-source synthetic --outdir ("artifacts\" + $t) --verbose
}
```

- Hydra (dados reais):
```
$env:HYDRA_IGNORE_CSV="1"; $env:HYDRA_IGNORE_CACHE="1"
foreach ($t in $tickers) {
  Write-Host "Rodando $t (hydra)..."
  python orchestrator\run_pipeline.py --ticker $t --engine full --data-source hydra --qual-source hydra --outdir ("artifacts\" + $t) --verbose
}
```

- Reunir PDFs num diretório final:
```
$dest = Join-Path $PWD "artifacts\_reports_20"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$today = (Get-Date).ToString('yyyy-MM-dd')
foreach ($t in $tickers) {
  $src = Join-Path $PWD ("artifacts\" + $t + "\" + $today + "\report.pdf")
  if (Test-Path $src) {
    Copy-Item $src (Join-Path $dest ("report_" + $t + ".pdf")) -Force
  } else {
    Write-Warning "Report não encontrado: $t"
  }
}
```

6) CLI Hydra v2 (coleta + RAG + MegaForecast + sumário)
- Na raiz `Hydra\`:
  - `python hydra_scraper\cli.py run-all --period recent --out_dir outputs --debug`
  - `python hydra_scraper\cli.py run-all --period recent --out_dir outputs --strict-real-data` (modo estrito)
- Saídas: `Hydra\outputs\*` (csv/jsonl/faiss/logs) e artefatos MegaForecast em `Hydra\outputs\megaforecast\*`

7) Testes (opcional)
- Em `Hydra\Hermes` (venv ativo): `pytest -q`

Notas e fallbacks
- Para bloquear qualquer fallback, use `--strict-real-data` (CLI/Orquestrador) ou `HYDRA_STRICT_REAL_DATA=1`.
- Sem `GOOGLE_API_KEY`: RAG/seleção/sumários usam heurísticas.
- Sem FMP/Reddit: ESG neutro e Reddit via RSS; segue.
- Sem FAISS: índices em memória/"none" (QA pode avisar, não quebra).
- Defina `USER_AGENT`/`SEC_USER_AGENT` com contato real para a SEC.

Windows e dependências (dicas)
- `faiss-cpu` é opcional no Windows (desativado por marcador no requirements). O RAG cai para backend em memória.
- `WeasyPrint` pode requerer libs do sistema; se a instalação falhar, mantenha o restante. O orquestrador gera um PDF placeholder se o motor de relatório não estiver disponível.

8) Modo cripto CZ (beta)
- 1. Gere o CSV `daily_kpis_crypto.csv` com preços em BRL:
  - Em `Hydra/Hermes`: `python Hermes/scripts/crypto_data.py --outputs-dir outputs_crypto --start-date 2024-01-01 --end-date 2025-11-01`
  - O script usa yfinance para baixar XRP, TRX, NEAR, DOT, SOL, TON, AVAX, SHIB e BTC em USD, converte para BRL com USDBRL=X e salva em `outputs_crypto/daily_kpis_crypto.csv`. Também baixa HASH11.SA como referência.
- 2. Gere o relatório no modo cripto (usa HASH11.SA como benchmark padrão e moeda BRL):
  - `python Hermes/scripts/build_manual_report.py --mode crypto --outputs-dir outputs_crypto --report-dir Hermes/reports_crypto --benchmark HASH11.SA --disable-llm`
  - Se quiser apontar para um CSV diferente, use `--prices-file Caminho/para/daily_kpis_crypto.csv`.
- As figuras Hydra (equity, volatilidade, VaR, correlação, radar, treemap) são salvas em `REPORT_DIR/figures`.
- 3. Gere o prior/forecast com o MegaForecast (modo cripto):
  - `python Hermes/scripts/generate_crypto_prior.py --daily-csv outputs_crypto/daily_kpis_crypto.csv --out-dir outputs_crypto/backtest --artifacts-root Hydra/Hydra/megaforecast/artifacts_crypto`
  - Isso roda o `run_all.py` parametrizado, produz `forecast_bundle.json` e `prior_payload.json` em `outputs_crypto/backtest/`.
- 4. Rodar o multiagente com backtest mensal (com presets e splits), apontando para o prior recém-gerado:
  - `python Hermes/scripts/crypto_multiagent.py --prices-file outputs_crypto/daily_kpis_crypto.csv --hash11-file outputs_crypto/hash11_prices.csv --out-dir outputs_crypto/backtest --scenarios moderado,agressivo --train-end 2024-06 --val-end 2024-12 --prior-file outputs_crypto/backtest/prior_payload.json --forecast-bundle outputs_crypto/backtest/forecast_bundle.json`
  - O script executa os agentes QuantForecast → Sentiment/CZ → Black-Litterman → Risk com time-lock, gera `weights_history.csv`, `daily_returns.csv`, `backtest_summary.json` e um `qualitative_scores.json` por cenário, além de copiar o prior/forecast para cada pasta. Depois rode o `build_manual_report.py --mode crypto --outputs-dir outputs_crypto/backtest/<preset> ...` apontando para o cenário desejado.

