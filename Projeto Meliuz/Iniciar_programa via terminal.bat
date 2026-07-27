@echo off
:: Define o encode para UTF-8 para exibir acentos corretamente
chcp 65001 >nul

echo ==========================================
echo    INICIANDO AVALIADOR DE TESTES A/B (CLI)
echo ==========================================
echo.

:: Garante que o terminal vai abrir na pasta onde o bat está localizado
cd /d "%~dp0"

:: Ativa o ambiente virtual (.venv)
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo [AVISO] Ambiente virtual .venv nao encontrado, usando python global...
)

:: Executa o main.py
python main.py

echo.
echo ==========================================
echo Processo finalizado.
pause