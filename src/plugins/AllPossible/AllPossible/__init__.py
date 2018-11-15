"""
This is where the implementation of the plugin code goes.
The AllPossible-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import random
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('AllPossible')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class AllPossible(PluginBase):
