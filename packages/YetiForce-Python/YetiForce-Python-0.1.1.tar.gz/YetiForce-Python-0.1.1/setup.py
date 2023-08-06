from setuptools import setup

setup(
    name='YetiForce-Python',
    version='0.1.1',
    description='YetiForce CRM Python API Wrapper',
    packages=['yetiforce_python'],
    author='Kajetan Bancerz',
    author_email='kajetan.bancerz@gmail.com',
    url='https://github.com/kbancerz/yetiforce-python',
    license=open('LICENSE').read(),
    #long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'requests>=2.21.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
