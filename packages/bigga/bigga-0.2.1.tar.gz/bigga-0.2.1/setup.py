from setuptools import setup, find_packages

__VERSION__ = '0.2.1'

setup(
    name='bigga',
    version=__VERSION__,
    description="A simple CLI tool to deploy Python & Node microservices on linux instaces. Built on top of invoke, fabric and patchwork.",  # NOQA
    long_description="Bigga - A simple, opinionanted deployment tool for Python & Node",  # NOQA
    url='https://github.com/reckonsys/bigga',
    author='dhilipsiva',
    author_email='dhilipsiva@pm.me',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='bigga reckonsys cli deploy deployment',
    packages=find_packages(),
    install_requires=[
        'invoke', 'fabric', 'patchwork'
    ],
    entry_points={
        'console_scripts': ['bigga = bigga.cli:program.run']
    }
)
