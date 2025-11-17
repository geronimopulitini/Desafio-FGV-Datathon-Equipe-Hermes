Execução Padrão com IA (Seleção Automática)

Pré-requisitos
- Venv ativo (crie em `Hydra/Hermes` e instale deps: `pip install -r requirements.txt && pip install -e .`)
- OPCIONAL: `GOOGLE_API_KEY` no `.env` para usar Gemini; sem a chave, a seleção usa heurísticas.

Comando único (seleciona N=20 e gera 1 relatório consolidado):
- `python hydra_scraper\cli.py run-all-report --period recent --n 20 --out_dir outputs --report_out Hermes\artifacts\ai_report --debug`

Saídas
- Seleção salva: `outputs/selected_assets.json`
- Relatório final: `Hermes/artifacts/ai_report/report.pdf` (e `report.html`)

Notas
- A coleta (quant/qual), RAG e sumários são executados automaticamente antes de montar o relatório.
- Em Windows sem FAISS/WeasyPrint, o pipeline tem fallbacks e gera PDF mesmo que seja placeholder.

