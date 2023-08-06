from bpg import Template,TemplateLibrary
import pytest

def testTemplateExpressionsAreEvaluted():
    desc = {'a':{'value':52}, 
            'c':{'value':'axds'}, 
            'formula':{'value':'{% a*b %}'}}
    template = Template(desc)
    
    conf = template.instantiate({'a':10, 'b':25});
    assert 'formula' in conf
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
    template.load('test-template.yml')
    conf = template.instantiate({'a':10, 'b':25});
    assert conf['formula'] == 250
    
def testFindSimpleProperty():
    template = Template()
    template.load('test-template.yml')
    p = template.find('formula')
    assert p is not None
    assert p['value'] == '{%a*b%}'
    assert p['display-name'] == 'Expression'
    
def testFindNestedProperty():
    template = Template()
    template.load('test-template.yml')
    p = template.find('section1.a')
    assert p is not None
    assert p['value'] == 75
    assert p['display-name'] == 'section1.a'

def testFindTemplateByName():
    lib = TemplateLibrary()
    assert lib.findTemplate("test") is not None
    
def testUnknownTemplate():
    lib = TemplateLibrary()
    with pytest.raises(ValueError) as e:
        lib.findTemplate("unknown") 

