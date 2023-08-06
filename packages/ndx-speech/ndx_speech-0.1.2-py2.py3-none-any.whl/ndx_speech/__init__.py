import os
from pynwb import load_namespaces, get_class
from os import path

name = 'speech'

here = path.abspath(path.dirname(__file__))
root = path.split(here)[0]
ns_path = os.path.join(root, 'spec', name + '.namespace.yaml')

load_namespaces(ns_path)

Transcription = get_class('Transcription', name)