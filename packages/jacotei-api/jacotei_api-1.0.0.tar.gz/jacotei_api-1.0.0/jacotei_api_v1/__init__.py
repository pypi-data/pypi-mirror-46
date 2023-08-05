#!/usr/bin/env python
"""Add all of the modules in the current directory to __all__"""
import os

__all__ = []
name = "jacotei_api"

for module in os.listdir(os.path.dirname(__file__)):
    if module != '__init__.py' and module[-3:] == '.py':
        __all__.append(module[:-3])
