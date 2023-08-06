from setuptools import setup

setup(
    name='AIConf',
    version='1.1.7',
    description='Config reader and Factory method provider to create instances from given configs',
    url='http://github.com/ai-systems/AIConf',
    author='AI Systems, University of Manchester',
    author_email='viktor.schlegel@manchester.ac.uk',
    license='MIT',
    packages=['aiconf'],
    zip_safe=False,
    setup_requires=["nose"],
    install_requires=["pyhocon", "overrides"],
    tests_require=["nose", "coverage"]
)
