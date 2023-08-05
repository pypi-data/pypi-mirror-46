from setuptools import setup, find_packages

from typed_environ import __version__

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
]
extra_dev = [
    *extra_test,
]
extra_ci = [
    *extra_test,
    'python-coveralls',
]

setup(
    name='typed-environ',
    version=__version__,
    description='Load environment variables with types',
    url='https://github.com/MichaelKim0407/typed-environ',
    license='MIT',
    author='Michael Kim',
    author_email='mkim0470@gmail.com',

    packages=find_packages(),

    extras_require={
        'test': extra_test,
        'dev': extra_dev,
        'ci': extra_ci,
    },

    classifiers=[
        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Software Development :: Libraries',
    ],
)
