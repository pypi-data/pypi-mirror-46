# -*- coding: UTF-8 -*-

from Pyautomators.runner_util import load_step_modules 
import os

def get_new_dirs(file):
    list_dir = os.listdir(os.path.dirname(file))
    new_list=[]
    for dir in list_dir:
        if not "." in dir:
            new_list.append(str(os.path.join(os.path.dirname(file),dir)))
    load_step_modules(new_list)