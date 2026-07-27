import os
import getpass
import time
from pathlib import Path
from dotenv import load_dotenv

from src.data_processor import processar_csv
from src.sheets_integrador import salvar_resultado_teste, salvar_relatorio_txt
from src.config import GOOGLE_SHEET_ID, salvar_sheet_id
from src.ia_agent import analyze_ab_test


def configurar_chave_api():
    """
    Verifica se a chave da API está configurada, caso não esteja, solicita ao usuário para inserir a chave.
    """ 
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Chave da API do Gemini não foi encontrada.")
        api_key = getpass.getpass("Cole sua chave API aqui e aperte Enter (ela ficará invisível por segurança): ").strip()
    
        if not api_key:
            raise ValueError("Chave da API é obrigatória para seguir com a análise.")
    
        with open(".env", "a", encoding="utf-8") as f:
            f.write(f"\nGEMINI_API_KEY={api_key}\n")
        print("✅ Chave salva no arquivo .env com sucesso!\n")
        
        os.environ["GEMINI_API_KEY"] = api_key


def exibir_menu(arquivos_csv):
    """
    Gera um menu interativo no terminal baseado nos arquivos encontrados.
    """
    print("\n" + "="*40)
    print("📊 MENU DE ANÁLISE DE TESTES A/B ")
    print("="*40)
    
    for i, arquivo in enumerate(arquivos_csv):
        print(f"[{i + 1}] Analisar apenas: {arquivo.name}")
        
    print(f"[{len(arquivos_csv) + 1}] Analisar TODOS os documentos em lote")
    print("[0] Sair ")
    print("-" * 40)
    
    return input("Escolha um NÚMERO: ").strip()


def configurar_google_sheets() -> bool:
    """
    Pergunta sobre a sincronização com o Google Sheets UMA ÚNICA VEZ por execução.
    """
    print("\n--- OPÇÕES DE EXPORTAÇÃO ---")
    resposta_sheets = input("Deseja sincronizar com o Google Sheets? (s/n): ").strip().lower()
    sincronizar_sheets = (resposta_sheets == 's' or resposta_sheets == 'sim')

    if sincronizar_sheets:
        if not GOOGLE_SHEET_ID:
            print("\nNenhuma planilha configurada ainda.")
            novo_id = input("Cole o ID ou URL da sua Planilha do Google: ").strip()
            salvar_sheet_id(novo_id)
            print("✅ Planilha salva com sucesso para as próximas vezes!")
        else:
            print(f"Planilha atual configurada: {GOOGLE_SHEET_ID}")
            trocar = input("Deseja usar outra planilha? (s/n): ").strip().lower()
            if trocar == 's' or trocar == 'sim':
                novo_id = input("Cole o NOVO ID ou URL da Planilha: ").strip()
                salvar_sheet_id(novo_id)
                print("✅ Nova planilha salva com sucesso!")

    return sincronizar_sheets


def executar_analise(caminho_arquivo: Path, sincronizar_sheets: bool):
    """
    Processa, analisa, salva o relatório em TXT e registra os dados no CSV/Sheets.
    """
    print(f"\n| Iniciando análise do arquivo: {caminho_arquivo.name} ... |")
    try:
        dados_para_ia = processar_csv(str(caminho_arquivo))
        
        print("⏳ Aplicando pausa de segurança para sobrecarga no agente de IA...")
        time.sleep(20)
        
        resultado_analise = analyze_ab_test(dados_para_ia)
        
        print(f"\n--- RESULTADO ({caminho_arquivo.name}) ---")
        print(resultado_analise)
        print("-" * 40)

        # Armazenamento em TXT
        salvar_relatorio_txt(caminho_arquivo.name, resultado_analise)
        
        # Conteúdo do CSV / Google Sheets
        if "[Segunda SAÍDA : DADOS PARA PLANILHA]" in resultado_analise:
            bloco = resultado_analise.split("[Segunda SAÍDA : DADOS PARA PLANILHA]")[1].strip()
            linhas = [l for l in bloco.split('\n') if l.strip() and not l.startswith('-')]
            
            if linhas:
                linha_dados = linhas[0]
                colunas = linha_dados.split('|') # Separador por pipe
                
                if len(colunas) >= 4:
                    nome_teste = colunas[0].strip()
                    descricao = colunas[1].strip()
                    resultado = colunas[2].strip()
                    decisao = colunas[3].strip()
                    
                    # Salva no CSV local e no Sheets
                    salvar_resultado_teste(
                        nome_teste=nome_teste, 
                        descricao=descricao, 
                        resultado=resultado, 
                        decisao=decisao, 
                        sincronizar_sheets=sincronizar_sheets
                    )
                else:
                    print("⚠️ A IA não estruturou corretamente os dados com '|'.")
        
    except Exception as e:
        print(f"| Ocorreu um erro ao analisar {caminho_arquivo.name}: {e} |")


def main():
    load_dotenv()
    
    try:
        configurar_chave_api()
    except Exception as e:
        print(e)
        return

    pasta_docs = Path("docs")
    
    if not pasta_docs.exists():
        print("❌ Erro: A pasta 'docs' não foi encontrada neste diretório.")
        return

    arquivos_csv = list(pasta_docs.glob("*.csv"))
    
    if not arquivos_csv:
        print("❌ Erro: Nenhum arquivo CSV encontrado na pasta 'docs'.")
        return

    while True:
        escolha = exibir_menu(arquivos_csv)
        
        if escolha == '0':
            print("\nSaindo do assistente... \n")
            break
            
        try:
            opcao = int(escolha)
            
            # 1. Escolheu um arquivo específico
            if 1 <= opcao <= len(arquivos_csv):
                arquivo_escolhido = arquivos_csv[opcao - 1]
                sincronizar_sheets = configurar_google_sheets()
                executar_analise(arquivo_escolhido, sincronizar_sheets)
                
            # 2. Escolheu analisar TODOS em lote
            elif opcao == len(arquivos_csv) + 1:
                print("\nIniciando análise em lote de todos os arquivos...")
                sincronizar_sheets = configurar_google_sheets()
                for arquivo in arquivos_csv:
                    executar_analise(arquivo, sincronizar_sheets)
                    
            else:
                print("❌ Opção inválida. Escolha um número do menu.")
                
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite apenas números.")


if __name__ == "__main__":
    main()