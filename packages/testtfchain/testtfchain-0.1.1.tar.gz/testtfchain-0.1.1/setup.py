try:
    from setuptools import setup
except ImportError:
    # can't have the entry_points option here.
    from distutils.core import setup
from setuptools import setup, find_packages

required = []
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='testtfchain',
    version='0.1.1',
    author="Glen De Cauwsemaecker",
    author_email="glen@threefold.tech",
    description='pythonic tfchain client',
    long_description='pythonic tfchain client',
    packages=find_packages(),
    url="https://github.com/glendc/tfchain-py",
    license='MIT License',
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
