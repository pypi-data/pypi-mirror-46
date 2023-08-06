'''
a template is definition for configuration data.
a template can have one or more sub-templates
identified by name
@author: pinaki.poddar
'''
import yaml

#EXPRESSION_REGEX = r'\{%(?P<exp>[a-zA-Z0-9_\+-\*%/]+)%\}'
RESERVED_PROPERTIES=['name', 'display-name', 'version', 'description']
class Template(object):
    def __init__(self, data={}):
        '''
          creates a template with given dictionary
          @params: dictionary value can be an expression
        '''
        self.sub_templates = {}
        self.data = copy.deepcopy(data)
        self.name = data.get('name', '') 
        
    def load(self, name, filename):
        '''
          loads template from given YAML file 
        '''
        self.name = name
        with open(filename, 'r') as f:
            self.data = yaml.load(f) 
       
    def instantiate(self, variables=None, ctx=None):
        '''
           instantiates this template to create a configuration.
           expressions are evaluated with given variables
           
           @params: variables dictionary of variable 
           name and value. If a variable is missing,
           an exception is raised
           @return:  configuration same as a dictionary 
           isomorphic to this template, except all expressions
           are evaluated by substituting given variables
        '''        
        conf = {}
        for k,v in self.data.iteritems():
            if (k in RESERVED_PROPERTIES): continue
            if (not isinstance(v, dict)):
                raise ValueError('property [' + k + '] is not a dict')
            
            if (k == 'templates'):
                for subk, subv in v.iteritems():
                    conf[subk] = Template(subv).instantiate(variables, ctx)
            else:
                if (not 'value' in v):
                    raise ValueError('''property [' + {0} + '] has no value'
                        Its value type is {1}'''.format(k, type(v)))
                value = v['value']
                print 'value of [{0}] is {1}'.format(k, value)
                exp = self.getExpression(value)
                if exp:
                    try:
                        conf[k] = eval(exp, variables)
                        print 'evaluated  to [{0}] for property [{1}]'.format(conf[k],k)
                    except Exception as err:
                        raise ValueError('can not evaluate ' + exp, err)
                else:
                    # literal
                    conf[k] = value
        return conf 
             
    def get(self, path):
        '''
        '''
        self.data.get(path);
        
    def getExpression(self, s): 
        if (not isinstance(s, basestring)): return False  
        if (not s.startswith('{%')): return False
        if (not s.endswith('%}')): return False
        return s[2:-2]
    
    def __str__(self):
        return self.name
