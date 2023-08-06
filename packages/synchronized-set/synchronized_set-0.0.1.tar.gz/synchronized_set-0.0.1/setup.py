# from distutils.core import setup
from setuptools import setup

setup(
    name='synchronized_set',
    packages=['synchronized_set'],
    version='0.0.1',
    license='BSD',
    description='A threadsafe set.',
    author='David Charles Morse',
    author_email='dcmorse@armarti.com',
    url='https://gitlab.com/dcmorse/python_synchronized_set',
    download_url='https://gitlab.com/dcmorse/python_synchronized_set/-/archive/master/python_synchronized_set-master.tar.gz',
    keywords=['set', 'synchronized', 'threadsafe', 'thread-safe', 'thread safe'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
