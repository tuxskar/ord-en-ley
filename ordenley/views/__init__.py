import os
import sys

def get_data_dev(ui_file):
    ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(ROOT, 'interfaces', ui_file)

def get_data_dev(ui_file):
    dir = os.path.join(sys.prefix,"local/ordenley/interfaces")
    return os.path.join(dir, ui_file)
