# inspetoria_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import perform_merge
import pandas as pd

class InspecaoDadosView(APIView):
    def get(self, request, format=None):
        df_merged = perform_merge()

        if df_merged.empty:
            return Response({"erro": "Não foi possível carregar os dados."}, status=400)

        # Realiza os cálculos e regras de negócio
        # Total de Funcionários Inspecionados por 'cod_checklist'
        total_funcionarios_inspecionados = df_merged.groupby('cod_checklist')['matricula_funcionario'].nunique().reset_index()
        total_funcionarios_inspecionados = total_funcionarios_inspecionados.rename(
            columns={'matricula_funcionario': 'total_funcionarios_inspecionados'}
        )

        # Total de Inspetores Inspecionados por 'cod_checklist'
        total_inspetores_inspecionados = df_merged.groupby('cod_checklist')['matricula_inspetor'].nunique().reset_index()
        total_inspetores_inspecionados = total_inspetores_inspecionados.rename(
            columns={'matricula_inspetor': 'total_inspetores_inspecionados'}
        )

        # Total de Contratos Inspecionados por 'cod_checklist'
        total_contratos_inspecionados = df_merged.groupby('cod_checklist')['desc_depto'].nunique().reset_index()
        total_contratos_inspecionados = total_contratos_inspecionados.rename(
            columns={'desc_depto': 'total_contratos_inspecionados'}
        )

        # Total de Função Inspecionados por 'cod_checklist'
        total_funcao_inspecionados = df_merged.groupby('cod_checklist')['desc_funcao'].nunique().reset_index()
        total_funcao_inspecionados = total_funcao_inspecionados.rename(
            columns={'desc_funcao': 'total_funcoes_inspecionadas'}
        )

        # Total de Coordenador Inspecionados por 'cod_checklist'
        total_coordenador_inspecionados = df_merged.groupby('cod_checklist')['nom_coordenador'].nunique().reset_index()
        total_coordenador_inspecionados = total_coordenador_inspecionados.rename(
            columns={'nom_coordenador': 'total_coordenadores_inspecionados'}
        )

        # Agrega todos os resultados em um dicionário
        results = {
            'total_funcionarios_inspecionados': total_funcionarios_inspecionados.to_dict('records'),
            'total_inspetores_inspecionados': total_inspetores_inspecionados.to_dict('records'),
            'total_contratos_inspecionados': total_contratos_inspecionados.to_dict('records'),
            'total_funcoes_inspecionadas': total_funcao_inspecionados.to_dict('records'),
            'total_coordenadores_inspecionados': total_coordenador_inspecionados.to_dict('records'),
        }

        return Response(results)

class DadosBrutosInspecao(APIView):
    def get(self, request, format=None):
        df_merged = perform_merge()

        if df_merged.empty:
            return Response({"erro": "Não foi possível carregar os dados."}, status=400)

        return Response(df_merged.to_dict('records'))