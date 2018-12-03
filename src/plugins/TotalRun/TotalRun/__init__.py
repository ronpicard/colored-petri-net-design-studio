"""
This is where the implementation of the plugin code goes.
The TotalRun-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import random
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('TotalRun')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TotalRun(PluginBase):

        
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        #global pos_fire
        #name = core.get_attribute(active_node, 'name')

        #logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        #core.set_attribute(active_node, 'name', 'newName')

        #commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        #logger.info('committed :{0}'.format(commit_info))

        pos_fire={}
        drains={}
        feeds={}
        def string_to_dict(input_string):
            logger.info('yeah....about that')
            dict_ret={}
            str_ar=input_string.split(';')
            logger.info('hmmm')
            for entry in str_ar:
                dict_ret[entry.split(':')[0]]=int(entry.split(':')[1])

            logger.info('k')
            return dict_ret

        def cap_string_to_dict(col_string, cap_string):
            dict_ret=string_to_dict(col_string)
            cap_ar=cap_string.split(';')
            for entry in cap_ar:
                try:
                    if dict_ret[entry.split(':')[0]]>int(entry.split(':')[1]):
                        dict_ret[entry.split(':')[0]]=int(entry.split(':')[1])
                except:
                    dict_ret[entry.split(':')[0]]=0
            return dict_ret

        def dict_add(tok_dict, col_string, cap_string):
            col_dict=cap_string_to_dict(col_string, cap_string)
            for entry in col_dict:
                if entry in tok_dict:
                    tok_dict[entry]=tok_dict[entry]+col_dict[entry]
                else:
                    tok_dict[entry]=col_dict[entry]
            return tok_dict    
        def per_thing(node):
            #global pos_fire
            #use nonlocal keyword here to make sure stuff works
            #for i in core.get_pointer_names(node):
            #    if i=='dst':
            try:
                dst_node=core.load_pointer(node, 'dst')
                src_node=core.load_pointer(node, 'src')
                dst_path=core.get_path(dst_node)
                src_path=core.get_path(src_node)
                meta_tr=core.get_meta_type(node)
                if core.get_attribute(meta_tr, 'name')=='PlaceToTransition':
                    #check if thing is enabled
                    thresh=core.get_attribute(dst_node, 'Tokens')
                    tokens=core.get_attribute(src_node, 'Tokens')
                    cap=core.get_attribute(node, 'Tokens')
                    #logger.info('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
                    #logger.info(thresh)
                    #logger.info(tokens)
                    #logger.info(cap)
                    if dst_path in pos_fire:
                        #logger.info('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
                        pos_fire[dst_path]=[pos_fire[dst_path][0], dict_add(pos_fire[dst_path][1], tokens, cap)]
                    else:
                        #logger.info('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
                        try:
                            pos_fire[dst_path]=[string_to_dict(thresh), cap_string_to_dict(tokens, cap)]
                        except Exception as e:
                            logger.info(e)
                            #logger.info(dst_path)
                            #logger.info(tokens)
                            #logger.info(cap)
                            #logger.info('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
                    #logger.info(len(pos_fire))
                    #for i in pos_fire:
                    #    logger.info(i)
                    #    logger.info(pos_fire[i])
                    #    logger.info('----------------------------------------------------------------------------------')
                    if dst_path in drains:
                        #logger.info('ROUND 2 BBYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
                        drains[dst_path].append((src_path, cap))
                    else:
                        #logger.info('i did it reddittttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
                        drains[dst_path]=[(src_path, cap)]
                else:
                    #this can be done later.
                    #this should figure out weight assignments on the other side
                    try:
                        weight=core.get_attribute(node, 'Tokens')
                        thresh_path=core.get_path(src_node)
                        if src_path in feeds:
                            feeds[src_path].append((dst_path, weight))
                        else:
                            feeds[src_path]=[(dst_path, weight)]
                    except Exception as e:
                        logger.info(core.get_path(node))
                        logger.info(e)
                        #logger.info("WHYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY DID THIS HAPPEN")
            except Exception as e:
                logger.info(core.get_path(node))
                logger.info(e)
                logger.info('NOT A POINTER NODE THINGY')
            
        max_iter=core.get_attribute(active_node, 'Iteration')
        for count in range(max_iter):
            pos_fire={}
            drains={}
            feeds={}
            self.util.traverse(active_node, per_thing)
            enabled=[]

            for i in pos_fire:
                logger.info(i)
                logger.info(pos_fire[i])
                logger.info('----------------------------------------------------------------------------------')

            for path, dicts in pos_fire.items():
                thresh=dicts[0]
                vals=dicts[1]
                add_this=True
                for key in thresh:
                    if key in vals:
                        if (vals[key]<thresh[key] and thresh[key]>0) or (vals[key]>= (-1)*thresh[key] and thresh[key]<0):
                            add_this=False
                            break
                        #else this requirement is satisfied
                    elif thresh[key]>0:
                        add_this=False
                        break
                    

                if add_this:
                    enabled.append(path)
            logger.info('HI I RAN HERE')
            logger.info(len(enabled))
            for i in enabled:
                logger.info(i)

            if len(enabled)==0:
                break
        
            meh=random.randint(0, len(enabled)-1)
            to_drain=drains[enabled[meh]]
            to_feed=feeds[enabled[meh]]

            logger.info('NOTICE ME SENPAI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            logger.info(drains)
            logger.info(to_drain)
            for d in to_drain:
                #logger.info(core.get_path(root_node))
                #logger.info(d)
                cur=core.load_by_path(root_node, d[0])
                token_list=[]
                if not d[1]=='':
                    to_change=core.get_attribute(cur, 'Tokens')
                    weights={}
                    if not to_change=='':
                        for entry in to_change.split(';'):
                            weights[entry.split(':')[0]]=int(entry.split(':')[1])
                    for entry in d[1].split(';'):
                        cur_key, cur_val=entry.split(':')
                        cur_val=int(cur_val)
                        if cur_key in weights:
                            if weights[cur_key]-cur_val>0:
                                token_list.append(cur_key+':'+str(weights[cur_key]-cur_val))
                core.set_attribute(cur, 'Tokens', ';'.join(token_list))


            for fe in to_feed:
                f=fe[0]
                
                weights={}
                str_ar=fe[1].split(';')
                logger.info('hmmm')
                for entry in str_ar:
                    weights[entry.split(':')[0]]=int(entry.split(':')[1])
                
                cur=core.load_by_path(root_node, f)
                to_change=core.get_attribute(cur, 'Tokens')

                if not to_change=='':
                    str_ar=to_change.split(';')
                    logger.info('we are at this path: {0}'.format(f))
                    logger.info('the following is to_change->{0}END'.format(to_change))
                    for entry in str_ar:
                        logger.info('the following is entry->{0}END'.format(entry))
                        if entry.split(':')[0] in weights:
                            weights[entry.split(':')[0]]=weights[entry.split(':')[0]]+int(entry.split(':')[1])
                        else:
                            weights[entry.split(':')[0]]=int(entry.split(':')[1])
            
                new_string=[]
                logger.info('heyo friendo find me pls')
                logger.info(to_change)
                logger.info('wat')
            
                for col in weights:
                    logger.info(col)
                    new_string.append(col+':'+str(weights[col]))
                core.set_attribute(cur, 'Tokens', (';').join(new_string))
        commit_info = self.util.save(root_node, self.commit_hash, 'master', 'Python plugin updated the model')
        logger.info('wrote change')
        
