'''
A template is a definition for configurable parameters.
The configurable parameter definitions in a template
can specify an expression, for example, 
    log_disk_size = {% percentage % database_size %}
instead of a constant:
    log_disk_size = 50GB
    
A template can be loaded from a YAML file.
---
name: test
display-name: a template for testing
version: 1.0.0
a: 
   name: A constant property
   display-name:
   description:
   version:
   value: 1234
b: 
   name: An expression property
   display-name:
   description:
   version:
   value: '{% x + y %}'
templates:
   sub-template1: 
      ....
   sub-template2: 
      ....
      
---
    
A template can nest one or more (sub)templates
via 'templates' property.

A template is a factory for configuration (which is a 
hierarchical key-value pairs such as JSON). A set 
a set of variables must be supplied 
to evaluate an expression.
 
@author: pinaki.poddar
'''
import yaml
import copy

RESERVED_PROPERTIES=['name', 'display-name', 'version', 'description']
class Template(object):
    def __init__(self, name='', data={}):
        '''
          creates a template with given dictionary
          @params: dictionary value can be an expression
        '''
        self.sub_templates = {}
        self.data = copy.deepcopy(data)
        self.name = name
        
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
           @return:  configuration has same keys.
           All expressions, however, 
           are evaluated by substituting given variables.
           A template field is a dictionary describing
           property metadata. The instantiated configuration
           is a set of key-value pairs.
        '''        
        conf = {}
        for k,v in self.data.iteritems():
            if (k in RESERVED_PROPERTIES): continue
            if (not isinstance(v, dict)):
                raise ValueError('property [' + k + '] is not a dict')
            
            if (k == 'templates'): # sub-templates
                for subk, subv in v.iteritems():
                    conf[subk] = Template(subk, subv).instantiate(variables, ctx)
            else: # property definitions
                if (not 'value' in v):
                    raise ValueError('''property [' + {0} + '] definition has no value'
                        Its value type is {1}'''.format(k, type(v)))
                value = v['value']
                exp = self.parseExpression(value)
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
             
            
    def parseExpression(self, s): 
        '''
        parses given string to an expression
        @return None if not an expression. 
        An expression is enclosed in {% %} markers 
        '''
        if (not isinstance(s, basestring)): return None  
        if (not s.startswith('{%')): return False
        if (not s.endswith('%}')): return False
        return s[2:-2]
    
    def find(self, path):
        '''
        finds a nested property of a sub-template
        by given path
        @param path: a dot-separated sequence of kety
        to a nested property/sub-template
        '''
        keys = path.split('.')
        rv = self.data
        for key in keys:
            if (not key in rv):
                if ('templates' in rv): 
                    rv = rv['templates']
                else:
                    raise ValueError('segment [{0}] in path [{1}] not found'.format(key, path))
            rv = rv[key]
        return rv

    def __str__(self):
        return self.name
