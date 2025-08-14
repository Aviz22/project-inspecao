# inspetoria_app/models.py
from django.db import models

class Inspecao(models.Model):
    des_equipe_cadastro = models.CharField(max_length=255, null=True, blank=True)
    nom_funcionario = models.CharField(max_length=255, null=True, blank=True)
    matricula_funcionario = models.CharField(max_length=255, primary_key=True)
    nom_coordenador = models.CharField(max_length=255, null=True, blank=True)
    nom_lider = models.CharField(max_length=255, null=True, blank=True)
    cod_checklist = models.CharField(max_length=255, null=True, blank=True)
    nom_func_inspetor = models.CharField(max_length=255, null=True, blank=True)
    matricula_inspetor = models.CharField(max_length=255, null=True, blank=True)
    data_inspecao = models.DateField(null=True, blank=True)
    tipo_formulario = models.CharField(max_length=255, null=True, blank=True)
    sit_folha = models.CharField(max_length=255, null=True, blank=True, db_column='Sit. Folha')
    possui_per = models.CharField(max_length=255, null=True, blank=True, db_column='Possui Per.?')
    desc_funcao = models.CharField(max_length=255, null=True, blank=True, db_column='Desc.Funcao')
    desc_depto = models.CharField(max_length=255, null=True, blank=True, db_column='Desc. Depto')
    status = models.CharField(max_length=255, null=True, blank=True)
    status_demissao = models.CharField(max_length=255, null=True, blank=True, db_column='Status Demissão')
    desc_mun_l = models.CharField(max_length=255, null=True, blank=True, db_column='Desc. Mun. L')
    cpf = models.CharField(max_length=255, null=True, blank=True)
    filial = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        # Esta classe Meta é opcional. Se você não planeja usar o ORM para criar a tabela,
        # apenas para a serialização, pode ignorá-la.
        verbose_name = "Inspeção SESMT"
        verbose_name_plural = "Inspeções SESMT"