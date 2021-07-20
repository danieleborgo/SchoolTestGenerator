from setuptools import setup

setup(
    name='SchoolTestGenerator',
    version='2.0',
    packages=['generator', 'generator.test', 'rebuilder'],
    url='https://github.com/danieleborgo/SchoolTestGenerator',
    license='GNU General Public License v3.0',
    author='Daniele Borgo',
    author_email='',
    description='This software is able to generate several school tests, eventually all different from each other.',
    install_requires=[
        'PyLaTeX>=1.4.1'
    ]
)
