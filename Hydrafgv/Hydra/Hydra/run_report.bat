@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Criando ambiente virtual em .venv...
    py -3 -m venv .venv || goto :error
)

call ".venv\Scripts\activate.bat"

echo [INFO] Instalando dependências...
python -m pip install --upgrade pip >nul
python -m pip install -r Hermes\requirements.txt || goto :error

echo [INFO] Gerando relatório manual (dados locais)...
python Hermes\scripts\build_manual_report.py --benchmark= || goto :error

echo [INFO] Gerando relatório com dados de mercado (Yahoo Finance)...
python Hermes\generate_report.py || goto :error

if not exist "output" mkdir "output"
copy /Y "Hermes\reports_20_manual\report.pdf" "output\report.pdf" >nul || goto :error

echo [SUCESSO] Relatório final disponível em output\report.pdf
goto :eof

:error
echo [ERRO] Pipeline interrompido.
exit /b 1
