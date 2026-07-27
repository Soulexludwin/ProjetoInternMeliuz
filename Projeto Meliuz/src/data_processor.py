import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def limpar_cifras(valor_str):
# função do arquivo: Limpar os valores e processar os valores monetários, convertendo-os para float e gerar um resumo agregado dos dados.

# Remove símbolos de moeda e converte para float.

    if pd.isna(valor_str):
        return 0.0
    
    if isinstance(valor_str, (int, float)):
       return float(valor_str)
        
    valor_limpo = str(valor_str).replace('R$', '').replace(' ', '')
    valor_limpo = valor_limpo.replace('.', '') 
    valor_limpo = valor_limpo.replace(',', '.') 
    
    try:
        return float(valor_limpo)
    except ValueError:
        logging.warning(f"Não foi possível converter o valor: {valor_str}")
        return 0.0
    
# Função para processar o arquivo CSV, limpando os valores monetários e retornando um DataFrame.
def processar_csv(caminho_arquivo):
    """
    Processa o arquivo CSV, limpando os valores monetários e retornando um DataFrame.
    """
    logging.info(f"Lendo dados do arquivo: {caminho_arquivo}")
    
    try:
        df = pd.read_csv(caminho_arquivo)
        # Lê o csv e dados, e gera um resumo agregado por grupo de teste
        colunas_financeiras = ['comissão', 'cashback', 'vendas totais']
        
        for col in colunas_financeiras:
            if col in df.columns:
                df[col] = df[col].apply(limpar_cifras)
            else:
                logging.warning(f"A coluna '{col}' não foi encontrada no arquivo CSV.")
        
        df_agrupado = df.groupby('Grupos de usuários').agg({
            'compradores': 'sum',
            'comissão': 'sum',
            'cashback': 'sum',
            'vendas totais': 'sum',
            'Parceiro': 'first'  # Mantém o nome do parceiro do primeiro registro do grupo
        }).reset_index()

        logging.info("Dados limpos e agregados com sucesso.")
        
        resumo_texto = df_agrupado.to_markdown(index=False)
        
        return resumo_texto
    
    except Exception as e:
        logging.error(f"Erro ao processar o CSV: {e}")
        raise e
