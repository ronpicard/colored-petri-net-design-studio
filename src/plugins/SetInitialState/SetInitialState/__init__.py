"""
This is where the implementation of the plugin code goes.
The SetInitialState-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import json
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('SetInitialState')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class SetInitialState(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        
        def per_node(node): 
            meta_type=core.get_attribute(core.get_meta_type(node),'name')
            name = core.get_attribute(node,'name')
            if(meta_type == 'Place'):
                places_dict[name] = core.get_attribute(node,'tokens')

        def set_init_state(node,places):
            core.set_attribute(node,'InitialState',places)

        def make_json_string(dictionary):
            return (str(json.dumps(dictionary, indent=4, separators=(',', ': '))))

        places_dict = {}
        self.util.traverse(active_node, per_node)
        set_init_state(active_node,make_json_string(places_dict))
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
