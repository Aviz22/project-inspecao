import os
import pandas as pd
import redshift_connector
from dotenv import load_dotenv
import numpy as np

load_dotenv()

def get_redshift_connection():
    """
    Estabelece a conexão com o Redshift usando as credenciais do .env.
    """
    try:
        conn = redshift_connector.connect(
            host=os.getenv("REDSHIFT_HOST"),
            port=int(os.getenv("REDSHIFT_PORT")),
            database=os.getenv("REDSHIFT_DB"),
            user=os.getenv("REDSHIFT_USER"),
            password=os.getenv("REDSHIFT_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Redshift: {e}")
        return None

def query_to_dataframe(query):
    """
    Executa uma query no Redshift e retorna um DataFrame do Pandas.
    """
    conn = get_redshift_connection()
    if conn is None:
        return pd.DataFrame()
        
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
        return df
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def get_cubo_inspecoes():
    """
    Extrai os dados do cubo res_funcionarios_inspecionados, conforme a documentação.
    """
    query_inspecoes = """
        SELECT
            des_equipe_cadastro, nom_funcionario, matricula_funcionario,
            nom_coordenador, nom_lider, cod_checklist,
            nom_func_inspetor, matricula_inspetor, data_inspecao,
            tipo_formulario
        FROM
            res_funcionarios_inspecionados;
    """
    df_inspecoes = query_to_dataframe(query_inspecoes)
    return df_inspecoes

def get_data_from_excel(file_path):
    """
    Lê o arquivo Excel (.xlsx) e retorna um DataFrame.
    """
    try:
        df_sra = pd.read_excel(file_path)
        return df_sra
    except FileNotFoundError:
        print(f"Erro ao ler o arquivo Excel: [Errno 2] No such file or directory: '{file_path}'")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erro inesperado ao ler o arquivo Excel: {e}")
        return pd.DataFrame()
        
def perform_merge():
    """
    Realiza o merge dos dados do cubo do Redshift com a planilha Excel.
    """
    df_inspecoes = get_cubo_inspecoes()
    df_sra = get_data_from_excel('SRA_NORTE_TECH.xlsx')

    if df_inspecoes.empty or df_sra.empty:
        return pd.DataFrame()

    # Renomeia a coluna 'Matricula' do Excel para fazer o merge
    df_sra = df_sra.rename(columns={'Matricula': 'matricula_funcionario'})
    
    # Converte a coluna 'matricula_funcionario' para string
    df_sra['matricula_funcionario'] = df_sra['matricula_funcionario'].astype(str)

    # Merge dos DataFrames
    df_merged = pd.merge(df_inspecoes, df_sra, on='matricula_funcionario', how='left')

    # Renomeia as colunas para o padrão do modelo Django
    df_merged = df_merged.rename(columns={
        'Sit. Folha': 'sit_folha',
        'Possui Per.?': 'possui_per',
        'Desc.Funcao': 'desc_funcao',
        'Desc. Depto': 'desc_depto',
        'Status Demissão': 'status_demissao',
        'Desc. Mun. L': 'desc_mun_l',
        'CPF': 'cpf',
        'Filial': 'filial',
        'Status': 'status'
    })
    
    # --- NOVO CÓDIGO: SUBSTITUI VALORES NaN POR None de forma mais robusta ---
    df_merged = df_merged.replace({np.nan: None})
    
    # Seleciona apenas as colunas finais
    final_columns = [
        'des_equipe_cadastro', 'nom_funcionario', 'matricula_funcionario',
        'nom_coordenador', 'nom_lider', 'cod_checklist', 'nom_func_inspetor',
        'matricula_inspetor', 'data_inspecao', 'tipo_formulario',
        'sit_folha', 'possui_per', 'desc_funcao', 'desc_depto',
        'status', 'status_demissao', 'desc_mun_l', 'cpf', 'filial'
    ]
    
    return df_merged[final_columns]