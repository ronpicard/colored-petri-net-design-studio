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
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


# resets the token values of the places to the values
# that they were when SetInitialState plugin ran
class Reset(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        branch = 'master'
        message = 'Python plugin updated the model'

        # called on each node
        def per_node(node):
            meta_type = core.get_attribute(core.get_meta_type(node), 'name')
            name = core.get_attribute(node, 'name')
            if(meta_type == 'Place'):
                if name in places_dict:
                    core.set_attribute(node, 'Tokens', str(places_dict[name]))
                else:
                    message = 'Place added after SetIniitalState plugin run'
                    logger.info('[INFO]: ' + message)

        # gets the initial state attribute on the network
        def get_init_state(node):
            name = core.get_attribute(node, 'name')
            if(name == 'Network'):
                return json.loads(core.get_attribute(node, 'InitialState'))
            else:
                logger.info('[INFO]: Not the Network node')

        # reset attribute on network
        def reset_addtribute(node, attribute):
            name = core.get_attribute(node, 'name')
            if(name == 'Network'):
                core.set_attribute(node, attribute, '')
            else:
                logger.info('[INFO]: Not the Network node')

        reset_addtribute(active_node, 'StateSpace')
        reset_addtribute(active_node, 'IsDeterministic')
        places_dict = get_init_state(active_node)
        self.util.traverse(active_node, per_node)
        self.util.save(root_node, self.commit_hash, branch, message)
