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
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


# sets the saves the token values of the places in currrent
# state so that when the rest plug runs, it will return the
# composition to these values
class SetInitialState(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        places_dict = {}
        branch = 'master'
        message = 'Python plugin updated the model'

        # called on each node
        def per_node(node):
            meta_type = core.get_attribute(core.get_meta_type(node), 'name')
            name = core.get_attribute(node, 'name')
            if(meta_type == 'Place'):
                places_dict[name] = core.get_attribute(node, 'Tokens')

        # sets the initial state attribute on the network
        def set_init_state(node, places_dict):
            name = core.get_attribute(node, 'name')
            if(name == 'Network'):
                core.set_attribute(node, 'InitialState', places_dict)
            else:
                logger.info('[INFO]: Not Network node')

        # make a json string from a dictionary
        def make_json_string(dictionary):
            json_obj = json.dumps(dictionary, indent=4, separators=(',', ': '))
            return (str(json_obj))

        self.util.traverse(active_node, per_node)
        set_init_state(active_node, make_json_string(places_dict))
        self.util.save(root_node, self.commit_hash, branch, message)
