# -*- coding: utf-8 -*-
import argparse

from orcautomators import created_dir, exec_file

'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
"""Importando bibliotecas internas"""
# - annotation:
# mainTitle: Pyautomators inLine
# text_description:
# - O modulo __main__ trabalha com a execução dos testes em linha de comando
# parameters:
# - string: "comando [CHAVE ARGUMENTOS]" 
# ex:
# - python: "python -m Pyautomators COMANDO [CHAVE ARGUMENTOS]"
# - python: "python -m Pyautomators criar_projeto -n Testes_Web\n"

"""So vai usar a main, caso este arquivo ou modulo seja chamado"""
if '__main__' == __name__:

    ARG = argparse.ArgumentParser()
    """criando um objeto para receber os argumentos"""

# - annotation:
# title:
###        - "**Comandos**\n"
# text_description:
###        - "**criar_projeto:** Usado para gerar projeto de automação e a arquitetura de diretório\n"
###        - "\t**CHAVES:** -f -d (Opcional)\n"
###        - "**execute:** Usado para executar um projeto orquestrado com base em um yaml\n"
###        - "\t**CHAVES:** -f -d (Opcional)\n"
###        - "**criar_doc:** Usado para gerar um documento de evidencia do projeto, com base no dos arquivos de resultados da pasta docs/reports"
###        - " as imagens para cada step deve conter o nome da funcionalidade, cenario e step no nome da imagem a qual ela pertence.\n"
###        - "\t**CHAVES:** -d(Opcional)\n"
###        - "**Master_Remote:** Usado para abrir um conector master para executar testes em clients remote\n"
###        - "\t**CHAVES:** -f \n"
###        - "**Client_Remote:** Usado para abrir um servidor master para executar testes\n"
###        - "\t**CHAVES:** -f \n"
###        - "**Gerar_zip:** Usado para abrir um servidor master para executar testes\n"

# - annotation:
###    title: "**Parametros**\n"
# text_description:
###        - "Os Parametros ou argumentos são passados para especificar a execução de um determinado comando.\n"
###        - "**-f ou --file_yaml:** Arquivo Yaml base para execucoes em threads e containers.\n"
###        - "**-n ou --nome_projeto:** Criar um projeto com a base do Pyautomators.\n"
###        - "**-d ou --diretorio:** Para indicar um diretorio para a execução das ações.\n"
###        - "**--volume_host:** Volume do host.\n"
###        - "**--volume_container:** Volume do container.\n"
###        - "**--master_host:** IP do master.\n"
###        - "**--instancia:** Instancia do Yaml a ser executada.\n"
###        - "**-i ou --retorn_result:** Retornar resultados.\n"
# ex:
# - python: "python -m Pyautomators execute -f data/run.yaml\n"
# - python: "python -m Pyautomators criar_projeto -n Testes_Web\n"

    """Adicionando os argumento"""
    ARG.add_argument("comando", help="")
    ARG.add_argument(
        "-n",
        '--name',
        required=False,
        help="Criar um projeto com a base do Pyautomators")
    ARG.add_argument(
        "-f",
        '--file_exec',
        required=False,
        default='Pyautomators.yaml',
        help="Identifica um arquivo para executar na pasta manager")

    PROJECT = vars(ARG.parse_args())

    """Chamadas de funcao para cada argumento"""
    if PROJECT['comando'] == 'create':
        created_dir.create_project(PROJECT["name"])

    elif PROJECT['comando'] == "exec":
        exec_file.orchestra(PROJECT['file_exec'])

    else:
        ERROR = """Undefined Command"""

        raise Exception(ERROR)
