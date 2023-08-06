from bpg import Template
def test_something():
    template = Template()
    template.load('test-template.yml')
    conf = template.instantiate({'a':10, 'b':25});
    print 'configuration:{0}'.format(conf)
    assert conf['formula'] == 250