from setuptools import setup




setup(
    name='TpModel',
    version='0.2',
    author='nbl',
    author_email='',
    url='',
    description=u'TpModel',
    packages=['TpModel'],
    install_requires=[],
    entry_points={
        "console_scripts": ['TpModel = CMD:cmd'
                            'TpModel = Config:config']
    }
)