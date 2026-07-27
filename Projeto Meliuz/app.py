import os
import time
from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from src.data_processor import processar_csv
from src.ia_agent import analyze_ab_test
from src.sheets_integrador import salvar_relatorio_txt, salvar_resultado_teste
from src.config import GOOGLE_SHEET_ID, salvar_sheet_id

load_dotenv()

# Estrutura da pagina do streamlit (DEVE SER O PRIMEIRO COMANDO DE INTERFACE)
st.set_page_config(page_title="Avaliador de Testes A/B - Méliuz", page_icon="🚀", layout="wide")

# ==========================================
# BARRA LATERAL (Sidebar) - Configurações
# ==========================================
st.sidebar.title("⚙️ Configurações Google Sheets")

usar_google_sheets = st.sidebar.checkbox("📊 Ativar sincronização", value=False)

if usar_google_sheets:
    # Mostra o campo de texto preenchido com o ID atual (se existir)
    input_sheet = st.sidebar.text_input("ID ou Link da Planilha", value=GOOGLE_SHEET_ID if GOOGLE_SHEET_ID else "")
    st.sidebar.text("E-mail do bot caso a planilha seja privada: melsheets@gen-lang-client-0646125612.iam.gserviceaccount.com")
    
    # Se o usuário digitar algo diferente do que está salvo, atualiza o .env
    if input_sheet and input_sheet != GOOGLE_SHEET_ID:
        salvar_sheet_id(input_sheet)
        st.sidebar.success("✅ Planilha atualizada!")

# Chave API na Sidebar
st.sidebar.markdown("---")
api_key_env = os.getenv("GEMINI_API_KEY")
if not api_key_env:
    st.sidebar.warning("⚠️ Chave da API do Gemini não encontrada no .env")
    api_key_input = st.sidebar.text_input("Cole sua chave API do Gemini:", type="password")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        api_key_env = api_key_input

# ==========================================
# CORPO PRINCIPAL DA APLICAÇÃO
# ==========================================
st.title("📊 Avaliador de Testes A/B (Gemini) ")
st.write("Faça o upload do arquivo CSV do parceiro para iniciar a análise estratégica automatizada.")
st.write("O modelo de IA irá analisar os dados e fornecer insights sobre qual variante é mais promissora, além de gerar um relatório executivo e registrar os resultados.")
st.write("⚠️ Certifique-se de que o arquivo CSV esteja no formato correto, conforme especificado na documentação do projeto.")

# Rodapé explicativo
st.caption("Não se preocupe se estiver demorando um pouco, o tempo médio de processamento é de aproximadamente 40 segundos.")
st.caption("Feito por Ryan Kaique, versão 0.4.6")

# Plano de fundo e estilos do texto
st.markdown(
    """
    <style>
    div[data-testid="stRadio"] label {
        padding: 10px 14px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="stRadio"] label p {
        font-size: 18px !important;
        font-weight: 500;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    .stApp {
        background: linear-gradient(135deg, #FC8EAC, #E75480, #1C0506);
        background-attachment: fixed;
    }
    div.stButton > button {
        font-size: 20px !important;
        font-weight: bold !important;
        height: 2.5em !important;
        width: 220px !important;
        background: linear-gradient(135deg, #1C0506, #E75480, #1C0506);
        color: white !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Caminho da pasta
pasta_docs = Path("docs")

# Modos de analise dos arquivos
modo = st.radio(
    "Selecione o modo de análise:",
    ["📁 Selecionar arquivo da pasta docs", "🚀 Analisar TODOS os arquivos da pasta docs (Lote)", "📤 Fazer Upload Manual de CSV"]
)

arquivos_para_processar = []

if modo == "📁 Selecionar arquivo da pasta docs":
    if pasta_docs.exists():
        arquivos_csv = list(pasta_docs.glob("*.csv"))
        if arquivos_csv:
            nomes_arquivos = [f.name for f in arquivos_csv]
            escolhido = st.selectbox("Escolha o arquivo:", nomes_arquivos)
            arquivos_para_processar = [pasta_docs / escolhido]
        else:
            st.warning("Nenhum arquivo CSV encontrado na pasta docs.")
    else:
        st.error("Pasta 'docs' não encontrada.")

elif modo == "🚀 Analisar TODOS os arquivos da pasta docs (Lote)":
    if pasta_docs.exists():
        arquivos_para_processar = list(pasta_docs.glob("*.csv"))
        st.info(f"📁 Encontrados {len(arquivos_para_processar)} arquivos para processamento em lote.")
    else:
        st.error("Pasta 'docs' não encontrada.")

elif modo == "📤 Fazer Upload Manual de CSV":
    arquivo_subido = st.file_uploader("Selecione o arquivo CSV do teste A/B", type=["csv"])
    if arquivo_subido:
        temp_path = f"temp_{arquivo_subido.name}"
        with open(temp_path, "wb") as f:
            f.write(arquivo_subido.getbuffer())
        arquivos_para_processar = [Path(temp_path)]

# ==========================================
# BOTÃO E PROCESSAMENTO DA ANÁLISE
# ==========================================
if arquivos_para_processar:
    
    # --- AQUI ESTÁ O BOTÃO DE AÇÃO ---
    if st.button("🚀 Iniciar Análise"):

        if not api_key_env:
            st.error("❌ Por favor, informe a chave da API do Gemini antes de continuar.")
        else:
            total_arquivos = len(arquivos_para_processar)
            
            for i, caminho_arq in enumerate(arquivos_para_processar):
                nome_exibicao = caminho_arq.name.replace("temp_", "")
                
                with st.spinner(f"Analisando ({i+1}/{total_arquivos}): {nome_exibicao}..."):
                    try:
                        dados_para_ia = processar_csv(str(caminho_arq))
                        
                        if total_arquivos > 1 and i > 0:
                            time.sleep(20)
                            
                        resultado_analise = analyze_ab_test(dados_para_ia)
                        
                        # Salva Relatório em TXT
                        salvar_relatorio_txt(nome_exibicao, resultado_analise)
                        
                        # Extrai a decisão e salva o registro
                        if "[Segunda SAÍDA : DADOS PARA PLANILHA]" in resultado_analise:
                            bloco_dados = resultado_analise.split("[Segunda SAÍDA : DADOS PARA PLANILHA]")[1].strip()
                            linhas = [linha for linha in bloco_dados.split('\n') if linha.strip() and not linha.startswith('-')]
                            if linhas:
                                linha_dados = linhas[0]
                                colunas = linha_dados.split('|')
                                if len(colunas) >= 4:
                                    # --- CORREÇÃO APLICADA AQUI (sincronizar_sheets) ---
                                    salvar_resultado_teste(
                                        nome_teste=colunas[0].strip(), 
                                        descricao=colunas[1].strip(), 
                                        resultado=colunas[2].strip(), 
                                        decisao=colunas[3].strip(),
                                        sincronizar_sheets=usar_google_sheets
                                    )
                        
                        st.success(f"✅ Análise concluída e salva com sucesso para: {nome_exibicao}")
                        
                        st.markdown("---")
                        st.subheader(f"📈 Panorama Visual das Variantes: {nome_exibicao}")
                        if isinstance(dados_para_ia, pd.DataFrame) and not dados_para_ia.empty:
                            st.bar_chart(dados_para_ia)
                        
                        partes = resultado_analise.split("[Segunda SAÍDA : DADOS PARA PLANILHA]")
                        relatorio_executivo = partes[0].replace("[Primeira SAÍDA : RELATÓRIO EXECUTIVO]", "").strip()
                        
                        with st.expander(f"📄 Ver Relatório Executivo Detalhado: {nome_exibicao}", expanded=(total_arquivos == 1)):
                            st.markdown(relatorio_executivo)
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao processar {nome_exibicao}: {e}")
                        
                if caminho_arq.name.startswith("temp_") and caminho_arq.exists():
                    os.remove(caminho_arq)