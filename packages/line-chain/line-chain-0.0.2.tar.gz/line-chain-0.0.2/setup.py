from setuptools import find_packages, setup

name = 'line-chain'
module = name.replace("-", "_")
setup(
    name=name,
    version='0.0.2',
    description='Value Scheduler based on Progress',
    url=f'https://github.com/FebruaryBreeze/{name}',
    author='SF-Zhou',
    author_email='sfzhou.scut@gmail.com',
    keywords='Scheduler Progress',
    packages=find_packages(exclude=['tests']),
    package_data={f'{module}': ['schema/*.json']},
    install_requires=[
        'jsonschema',
        'json-schema-to-class>=0.1.7',
    ]
)
