"""
Flask-Cerberus
-------------
Add Cerberus validation to Flask

"""
from setuptools import setup

setup(
    name='FlaskCerberus',
    version='0.1rc',
    url='http://github.com/atlanteanio/FlaskCerberus/',
    license='',
    author='Dan Sikes',
    author_email='dsikes@atlantean.io',
    description='Add Cerberus validation to Flask',
    long_description="Add Cerberus validation to Flask",
    packages=['FlaskCerberus'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'cerberus'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)