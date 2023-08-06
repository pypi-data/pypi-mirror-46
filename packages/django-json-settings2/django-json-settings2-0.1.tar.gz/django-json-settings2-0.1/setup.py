import os
from setuptools import setup, find_packages


project_name = 'django-json-settings2'

if os.path.exists('README.rst'):
    long_description = open('README.rst', 'r').read()
else:
    long_description = \
        'See https://bitbucket.org/netlandish/django-json-settings2/'


setup(
    name=project_name,
    version=__import__('json_settings2').get_version(),
    packages=find_packages(),
    description='Set, and save, Django settings to json formatted files.',
    author='Netlandish Inc.',
    author_email='hello@netlandish.com',
    url='https://bitbucket.org/netlandish/django-json-settings2/',
    long_description=long_description,
    platforms=['any'],
    install_requires=['Django>=1.11'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Web Environment',
    ],
    include_package_data=True,
)
