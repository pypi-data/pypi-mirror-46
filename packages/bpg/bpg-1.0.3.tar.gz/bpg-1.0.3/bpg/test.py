from bpg import Template
import pytest

def testTemplateExpressionsAreEvaluted():
    desc = {'a':{'value':52}, 
            'c':{'value':'axds'}, 
            'formula':{'value':'{% a*b %}'}}
    template = Template('test', desc)
    
    conf = template.instantiate({'a':10, 'b':25});
    assert 'formula' in conf
    assert conf['formula'] == 250
    
def test_templateConstants():
    desc = {
        'a':{'value':52}, 
        'c':{'value':'axds'}
    }
    template = Template('test', desc)
    conf = template.instantiate();
    assert conf['a'] == 52
    
def test_templateNested():
    desc = {'a':{'value':52}, 
            'templates':{
                'nested':{'x':{'value':'{%a+b%}'}}
            }}
    template = Template('test', desc)
    
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['nested']['x'] == 35
    
def test_templateStringConcatenation():
    desc = {'formula':{'value':'{% a+b %}'}}
    template = Template('test', desc)
    
    conf = template.instantiate({'a':'this', 'b':' is a test'});
    assert conf['formula'] == 'this is a test'

def test_templateMissingVaraible():
    desc = {'a':{'value':52}, 
            'c':{'value':'axds'}, 
            'formula':{'value':'{% a*b*y %}'}}
    template = Template('test', desc)
    with pytest.raises(ValueError) as e:
        conf = template.instantiate({'a':'this', 'b':' is a test'});


def test_templateInternalVaraible():
    desc = {'a':{'value':'A'}, 
            'b':{'value':'B'}, 
            'formula':{'value':'{% a+b %}'}}
    template = Template('test', desc)
    conf = template.instantiate({'a':'external', 'b':' var'});
    assert conf['formula'] == 'external var'
    
def testLoadTemplate():
    template = Template()
    template.load('load-test', 'test-template.yml')
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['formula'] == 250
    
def testFindSimpleProperty():
    template = Template()
    template.load('find-test', 'test-template.yml')
    p = template.find('formula')
    assert p is not None
    assert p['value'] == '{%a*b%}'
    assert p['display-name'] == 'Expression'
    
def testFindNestedProperty():
    template = Template()
    template.load('find-test', 'test-template.yml')
    p = template.find('section1.a')
    assert p is not None
    assert p['value'] == 75
    assert p['display-name'] == 'section1.a'

