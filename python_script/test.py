# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
from walk_dir import *
import os

if __name__ == "__main__":
    for dir, list_dir, file in walk_dbsta('/home/andrey/work_dir/++.prj/create_ved/python_script'):
        print(get_list_sheet(os.path.join(dir,file)))

