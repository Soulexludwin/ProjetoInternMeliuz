import os
import time
from pathlib import Path
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from src.data_processor import processar_csv
from src.ia_agent import analyze_ab_test
from src.sheets_integrador import salvar_relatorio_txt, salvar_resultado_teste

load_dotenv()

# Estrutura da pagina do streamlit
st.set_page_config(page_title="Avaliador de Testes A/B - Méliuz", page_icon="🚀", layout="wide")

st.title("📊 Avaliador de Testes A/B (Gemini) ")
st.write("Faça o upload do arquivo CSV do parceiro para iniciar a análise estratégica automatizada.")
st.write("O modelo de IA irá analisar os dados e fornecer insights sobre qual variante é mais promissora, além de gerar um relatório executivo e registrar os resultados.")
st.write("⚠️ Certifique-se de que o arquivo CSV esteja no formato correto, conforme especificado na documentação do projeto.")

# Rodapé explicativo
st.caption("Não se preocupe se estiver demorando um pouco, o tempo médio de processamento é de aproximadamente 40 segundos.")
st.caption("Feito por Ryan Kaique, versão 0.4.6")

# Plano de fundo e estilos corporativos aprimorados para melhor padronização visual
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

# Chave API
api_key_env = os.getenv("GEMINI_API_KEY")
if not api_key_env:
    st.sidebar.warning("⚠️ Chave da API do Gemini não encontrada no .env")
    api_key_input = st.sidebar.text_input("Cole sua chave API do Gemini:", type="password")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        api_key_env = api_key_input

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

# Mensagens e Processos
if arquivos_para_processar:
    if st.button("🚀 Iniciar Análise"):
        if not api_key_env:
            st.error("❌ Por favor, informe a chave da API do Gemini antes de continuar.")
        else:
            total_arquivos = len(arquivos_para_processar)
            
            for i, caminho_arq in enumerate(arquivos_para_processar):
                nome_exibicao = caminho_arq.name.replace("temp_", "")
                
                with st.spinner(f"Analisando ({i+1}/{total_arquivos}): {nome_exibicao}..."):
                    try:
                        # 1. Processa o CSV e extrai os dados estruturados pelo Python
                        dados_para_ia = processar_csv(str(caminho_arq))
                        
                        if total_arquivos > 1 and i > 0:
                            time.sleep(20)
                            
                        # 2. Executa a IA para gerar o relatório estratégico
                        resultado_analise = analyze_ab_test(dados_para_ia)
                        
                        # 3. Salva os artefatos localmente (Relatório TXT com timestamp e CSV acumulativo)
                        salvar_relatorio_txt(nome_exibicao, resultado_analise)
                        
                        if "[Segunda SAÍDA : DADOS PARA PLANILHA]" in resultado_analise:
                            bloco_dados = resultado_analise.split("[Segunda SAÍDA : DADOS PARA PLANILHA]")[1].strip()
                            linhas = [linha for linha in bloco_dados.split('\n') if linha.strip() and not linha.startswith('-')]
                            if linhas:
                                linha_dados = linhas[0]
                                colunas = linha_dados.split('|')
                                if len(colunas) >= 4:
                                    salvar_resultado_teste(colunas[0].strip(), colunas[1].strip(), colunas[2].strip(), colunas[3].strip())
                        
                        st.success(f"✅ Análise concluída para: {nome_exibicao}")
                        
                        # 4. Exibição Visual dos Gráficos com base nos dados tratados pelo Python
                        st.markdown("---")
                        st.subheader(f"📈 Panorama Visual das Variantes: {nome_exibicao}")
                        # Exibe um gráfico de barras comparativo direto na interface web
                        if isinstance(dados_para_ia, pd.DataFrame) and not dados_para_ia.empty:
                            st.bar_chart(dados_para_ia)
                        
                        # 5. Tratamento e exibição limpa do Relatório Executivo da IA
                        partes = resultado_analise.split("[Segunda SAÍDA : DADOS PARA PLANILHA]")
                        relatorio_executivo = partes[0].replace("[Primeira SAÍDA : RELATÓRIO EXECUTIVO]", "").strip()
                        
                        with st.expander(f"📄 Ver Relatório Executivo Detalhado: {nome_exibicao}", expanded=(total_arquivos == 1)):
                            st.markdown(relatorio_executivo)
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao processar {nome_exibicao}: {e}")
                        
                if caminho_arq.name.startswith("temp_") and caminho_arq.exists():
                    os.remove(caminho_arq)