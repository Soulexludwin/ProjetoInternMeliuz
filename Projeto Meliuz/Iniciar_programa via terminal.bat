@echo off
chcp 65001 >nul

echo ==========================================
echo    INICIANDO AVALIADOR DE TESTES A/B (CLI)
echo ==========================================
echo.

cd /d "%~dp0"

if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo [AVISO] Ambiente virtual .venv nao encontrado, usando python global...
)

python main.py

echo.
echo ==========================================
echo Processo finalizado.
pause