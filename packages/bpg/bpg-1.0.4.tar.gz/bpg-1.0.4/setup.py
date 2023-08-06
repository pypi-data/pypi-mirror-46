from distutils.core import setup
setup(
    name='bpg',
    packages = ['bpg'],
    version = '1.0.4',
    url='http://era.nutanix.com',
    license='Apache 2.0',
    long_description='Template engine\nwith Expression Support',
    description='template engine with expression',
    author='nobody',
    author_email='era@nutanix.com',
    install_requires = ['pyyaml']
)