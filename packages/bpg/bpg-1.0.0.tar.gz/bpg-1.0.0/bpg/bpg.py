'''
Created on May 3, 2019

@author: pinaki.poddar
'''
import yaml
'''
a template is definition for configuration data.
a template can have one or more sub-templates
identified by name

'''
class Template(object):
    def __init__(self):
        self.sub_templates = {}
        
    def load(self, filename):
        with open(filename, 'r') as f:
            self.data = yaml.load(f) 
       
    def instantiate(self, variables=None, ctx=None):
        '''
           instantiates this template to create a configuration.
           
           params: 
           
        '''        
        conf = {}
        for k,v in self.data.iteritems():
            if isinstance(v, dict):
                pass
            else:
                try:
                    conf[k] = eval(v, variables)
                except:
                    conf[k] = v
        return conf 
             
    def get(self, path):
        self.data.get(path);
       
