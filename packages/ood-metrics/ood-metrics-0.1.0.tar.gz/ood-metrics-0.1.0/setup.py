from setuptools import setup

setup(
    name='ood-metrics',
    version='0.1.0',
    author='Taylor Denouden',
    author_email='taylordenouden@gmail.com',
    packages=['ood_metrics'],
    url='http://pypi.python.org/pypi/OODMetrics/',
    license='LICENSE',
    description='Calculate common OOD detection metrics',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy>=1.15.3",
        "matplotlib>=3.0.1",
        "scikit-learn>=0.20.0",
    ],
)