# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''

import os
import re


''' Este modulo trabalha com a construção do padrão de projeto Pyautomators em BDD,
    pode conter estrutural e tatico do projeto'''


def create_project(nome_projeto, diretorio=None):
    '''Este metodo abre um projeto em com a estrutura pyautomators

    parametros:
    nome_projeto(obrigatorio):precisa ser passado o nome da pasta que cera criada para o projeto, sendo ela não existente
    diretorio:em qual caminho ou diretorio vai ser criada a pasta, se não for passado vai ser criado no atual
    Exemplo:
    Criar_Projeto("novo projeto","C:/APP")
    Criar_Projeto("novo projeto")
    Criar_Projeto("novo projeto",Ambiente.path_atual())
    '''
    ##########################################################################
    #          Criando a pasta que contera o diretorio principal do projeto          #
    ##########################################################################

    os.mkdir(nome_projeto)

    os.chdir(nome_projeto)
    ##########################################################################
    #      Gerando as pastas que contera as responsabilidades do projeto             #
    ##########################################################################

    lista_pastas_principal = [
        "bin",
        "data",
        "docs",
        "driver",
        "features",
        "lib",
        'log',
        "steps",
        "manager",
        "docs/reports",
        "data/images",
        "pages",
        "pages/navigations",
        "pages/pages"]
    for lin in lista_pastas_principal:
        os.mkdir(lin)

    text = open("__init__.py", "w")
    text.close()

    text = open("manager/__init__.py", "w")
    text.close()
    ##########################################################################
    #            Escrevendo a estrutura do arquivo environment.py                    #
    ##########################################################################
    text = open("environment.py", "w")
    text.writelines(
        '"""\tPyautomators an Framework to Test \n\n\t\t\tProject: {}"""\n\n'.format(nome_projeto))
    text.writelines(
        'from Pyautomators import fixture\nfrom Pyautomators.contrib.scenario_autoretry import scenario_retry\n')
    text.writelines("def before_all(context):\n\tpass\n\n")
    text.writelines("def before_feature(context,feature):\n\tpass\n\n")
    text.writelines("def before_scenario(context,scenario):\n\tpass\n\n")
    text.writelines("def before_tag(context,tag):\n\tpass\n\n")
    text.writelines("def after_tag(context,tag):\n\tpass\n\n")
    text.writelines("def before_step(context,step):\n\tpass\n\n")
    text.writelines("def after_step(context,step):\n\tpass\n\n")
    text.writelines("def after_scenario(context,scenario):\n\tpass\n\n")
    text.writelines("def after_feature(context,feature):\n\tpass\n\n")
    text.writelines("def after_all(context):\n\tpass\n\n")
    text.close()
    
    text = open("steps/__init__.py", "w")
    text.close()

    text = open("pages/__init__.py", "w")
    text.close()

    text = open("pages/navigations/__init__.py", "w")
    text.close()

    text = open("pages/pages/__init__.py", "w")
    text.close()
