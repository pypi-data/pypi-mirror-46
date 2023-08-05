from setuptools import setup
from codecs import open
from os import path

setup(
    name='tornadoql',
    version='0.1.7',
    packages=['tornadoql'],
    url='https://github.com/deep-compute/tornadoql',
    license='MIT',
    keywords=['graphql', 'graphene', 'python', 'tornado'],
    author='deep-compute',
    author_email='support@deepcompute.com',
    description='GraphQL API for dev and hosting using Graphene and Tornado',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4'
    ],
    install_requires=[
        'basescript==0.2.8',
        'graphene==2.1.3',
        'tornado>=5.1.1',
        'deeputil==0.2.5',
        'Rx==1.6.1'
    ],
    package_data={
        'tornadoql': ['static/graphiql.html'],
    },
    entry_points={
        "console_scripts": [
            "tornadoql = tornadoql:main",
        ]
    }
)
