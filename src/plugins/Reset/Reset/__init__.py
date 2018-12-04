"""
This is where the implementation of the plugin code goes.
The Reset-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import json
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('Reset')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Reset(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        def per_node(node): 
            meta_type=core.get_attribute(core.get_meta_type(node),'name')
            name = core.get_attribute(node,'name')
            if(meta_type == 'Place'):
                if name in places_dict:
                    core.set_attribute(node,'Tokens',str(places_dict[name]))
                else:
                    logger.info('[ERROR]: Place must have been added after SetIniitalState plugin has run')

        def get_init_state(node):
            name=core.get_attribute(node,'name')
            if(name == 'Colored Petri Net'):
                return json.loads(core.get_attribute(node,'InitialState'))
            else:
                logger.info('[ERROR]: Not a the Colored Petri Net node')

        places_dict = get_init_state(active_node)
        self.util.traverse(active_node, per_node)
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
    