try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cassette_django',
    version='0.0.1',
    author='Joachim Lindqvist',
    author_email='lindqvist.joachim@gmail.com',
    packages=[
        'cassette_django',
        'cassette_django.management',
        'cassette_django.management.commands',
    ],
    scripts=[],
    install_requires=[
        'requests',
        'Django >= 1.8.0',
        'requests_toolbelt',
    ]
)