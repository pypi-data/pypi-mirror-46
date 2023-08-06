# -*- coding: utf-8 -*-

from djangoplus.db import models
from enderecos.db.fields import CepField


class Regiao(models.Model):
    nome = models.CharField('Nome', search=True, example='Norte')
    codigo = models.CharField('Código', search=True, example='1')

    fieldsets = (('Dados Gerais', {'fields': ('nome', 'codigo')}),)

    class Meta:
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'

    def __str__(self):
        return '{}'.format(self.nome)


class Estado(models.Model):
    nome = models.CharField('Nome', search=True, example='Acre')
    sigla = models.CharField('Sigla', search=True, example='AC')
    codigo = models.CharField('Código', search=True, example='11')
    regiao = models.ForeignKey(Regiao, verbose_name='Região', null=True, blank=False, filter=True, example='Norte')

    fieldsets = (('Dados Gerais', {'fields': ('nome', ('sigla', 'codigo'), 'regiao')}),)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        list_per_page = 50

    def __str__(self):
        return '{}'.format(self.sigla)


class Municipio(models.Model):
    nome = models.CharField(verbose_name='Nome', search=True, example='Rio Branco')
    estado = models.ForeignKey(Estado, verbose_name='Estado', filter=True, example='Acre')
    codigo = models.CharField('Código', search=True, example='1200401')

    fieldsets = (('Dados Gerais', {'fields': ('estado', 'nome', 'codigo')}),)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'
        list_per_page = 100

    def __str__(self):
        return '{}/{}'.format(self.nome, self.estado)


class Endereco(models.Model):
    cep = CepField('CEP', example='59.080-060')
    logradouro = models.CharField('Logradouro', example='Rua Professora Gipse Montenegro')
    numero = models.CharField('Número', example=123)
    complemento = models.CharField('Complemento', null=True, blank=True, example='Apartamento 101, Torre A')
    municipio = models.ForeignKey(Municipio, verbose_name='Município', filter=True, example='Natal', lazy=True)
    bairro = models.CharField('Bairro', example='Capim Macio')

    fieldsets = (('Dados Gerais', {'fields': (('cep', 'numero'), ('complemento', 'logradouro'), ('bairro', 'municipio'))}),)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return self.pk and '{}, {}, {}'.format(self.logradouro, self.numero, self.municipio) or None

