# -*- coding: utf-8 -*-
import os
import threading

import yaml
from Pyautomators.__main__ import main

'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
"""Importando bibliotecas internas"""


class GenericModel():

    def __init__(self, dict_yaml):
        self.dict_yaml = dict_yaml
        self.exec_options = []

        for option in self.dict_yaml:
            if option == 'Name' or option == 'name':
                self.exec_options.append("-Dname=" + self.dict_yaml[option])
            elif option == 'Tags' or option == 'tags':
                for arg in self.dict_yaml[option]:
                    tag_string = str(",").join(self.dict_yaml[option])
                self.exec_options.append("--tags=" + tag_string)
            elif option == 'Args' or option == 'args':
                for arg in self.dict_yaml[option]:
                    self.exec_options.append(
                        '-D' + str(arg) + '=' + str(self.dict_yaml[option][arg]))
    
    def get_feauture(self):

        for iten in self.dict_yaml.items():
            if iten[0] in ['Feature','feature']:
                self.exec_options.append(iten[1])
                break
        
class WebModel(GenericModel):

    def options_web(self, browser):
        name=self.dict_yaml['Name']
        self.exec_options.append('-Dbrowser=' + browser)

        for option in self.dict_yaml:
            if option == 'Reports' or option == 'reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append('--junit-directory={dir}{name}/xml/{browser}/'.format(dir=dir,name=name,browser=str(browser)))
                self.exec_options.append('--format=json')
                self.exec_options.append("-o={dir}{name}/{browser}-{name}.json".format(dir=dir,name=name,browser=str(browser)))
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append("-o={dir}cucumber/{browser}-{name}-cucumber.json".format(dir=dir,name=name,browser=str(browser)))

            elif option == "Spec" or option == 'spec':
                dir = "docs/spec/"
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append('-o={dir}{browser}-{name}/'.format(dir=dir,browser=browser,name=name))
                
        self.get_feauture()

        return self.exec_options


class MobileModel(GenericModel):

    def options_mobile(self, device):
        name=self.dict_yaml['Name']
        self.exec_options.append('-Ddevice=' + device)        
        for option in self.dict_yaml:
            if option == 'Reports' or option == 'reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append('--junit-directory={dir}{name}/xml/{device}/'.format(dir=dir,name=name,device=str(device)))
                self.exec_options.append('--format=json')
                self.exec_options.append("-o={dir}{name}/{device}-{name}.json".format(dir=dir,name=name,device=str(device)))
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append("-o={dir}cucumber/{device}-{name}-cucumber.json".format(dir=dir,name=name,device=str(device)))

            elif option == "Spec" or option == 'spec':
                dir = "docs/spec/"
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append('-o={dir}{device}-{name}/'.format(dir=dir,device=device,name=name))
                
        self.get_feauture()

        return self.exec_options


class DesktopModel(GenericModel):

    def run_desktop(self):
        name=self.dict_yaml['Name']
        for option in self.dict_yaml:
            if option == 'Reports' or option == 'reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append('--junit-directory={dir}{name}/xml/'.format(dir=dir,name=name))
                self.exec_options.append('--format=json')
                self.exec_options.append("-o={dir}{name}/{name}.json".format(dir=dir,name=name))
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append("-o={dir}cucumber/{name}-cucumber.json".format(dir=dir,name=name))

            elif option == "Spec" or option == 'spec':
                dir = "docs/spec/"
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append('-o={dir}{name}/'.format(dir=dir,name=name))
                
        self.get_feauture()

        return self.exec_options

class ThreadRun(threading.Thread):
    def __init__(self, options, sub_option=None):
        threading.Thread.__init__(self)
        self.sub_option = sub_option
        self.options = options

class ThreadWeb(ThreadRun):
    def run(self):
        main(WebModel(self.options).options_web(self.sub_option))
        

class ThreadMobile(ThreadRun):
    def run(self):
        main(MobileModel(self.options).options_mobile(self.sub_option))


class ThreadDesktop(ThreadRun):
    def run(self):
        main(DesktopModel(self.options).run_desktop())


def orchestra(file):
    file = open("manager/{file_yaml}".format(file_yaml=file), "r")
    block_test = yaml.load(file)
    
    def prepare_execute(keys_yaml):
        thread_list=[]
        for key,value in keys_yaml.items():
            
            if key in ['Type','type']:
                
                if value in ["Web",'web']:
                    for key,value in keys_yaml.items():
                        
                        if key in ['Browsers','browsers']:
                            for browser in value:
                                thread_list.append(ThreadWeb(keys_yaml, browser))
                    break

                elif value in ["Mobile",'mobile']:
                    for key,value in keys_yaml.items():
                        if key in ['Devices','devices']:
                            for device in value:
                                thread_list.append(ThreadMobile(keys_yaml, device))
                    break
                    
                elif value in ["Desktop",'desktop']:
                    thread_list.append(ThreadDesktop(keys_yaml))
                    break

                else:
                    ERROR = """Undefined Type"""
                    raise Exception(ERROR)
        return thread_list


    for test in block_test:
        
        if str(test).find("Test") != -1 or str(test).find("test") != -1:
            
            for block in prepare_execute(block_test[test]):
                block.start()


        else:
            ERROR = """Undefined Test"""
            Exception(ERROR)
