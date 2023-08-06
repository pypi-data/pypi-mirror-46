from bpg import Template
import pytest

def testTemplateExpressionsAreEvaluted():
    desc = {'a':{'value':52}, 
            'c':{'value':'axds'}, 
            'formula':{'value':'{% a*b %}'}}
    template = Template(desc)
    
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['formula'] == 250
    
def test_templateConstants():
    desc = {
        'a':{'value':52}, 
        'c':{'value':'axds'}
    }
    template = Template(desc)
    conf = template.instantiate();
    assert conf['a'] == 52
    
def test_templateNested():
    desc = {'a':{'value':52}, 
            'templates':{
                'nested':{'x':{'value':'{%a+b%}'}}
            }}
    template = Template(desc)
    
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['nested']['x'] == 35
    
def test_templateStringConcatenation():
    desc = {'formula':{'value':'{% a+b %}'}}
    template = Template(desc)
    
    conf = template.instantiate({'a':'this', 'b':' is a test'});
    assert conf['formula'] == 'this is a test'

def test_templateMissingVaraible():
    desc = {'a':{'value':52}, 
            'c':{'value':'axds'}, 
            'formula':{'value':'{% a*b*y %}'}}
    template = Template(desc)
    with pytest.raises(ValueError) as e:
        conf = template.instantiate({'a':'this', 'b':' is a test'});


def test_templateInternalVaraible():
    desc = {'a':{'value':'A'}, 
            'b':{'value':'B'}, 
            'formula':{'value':'{% a+b %}'}}
    template = Template(desc)
    conf = template.instantiate({'a':'external', 'b':' var'});
    assert conf['formula'] == 'external var'
    
def testLoadTemplate():
    template = Template()
    template.load('load-test', 'test-template.yml')
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['formula'] == 250
