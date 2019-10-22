import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-admin-chat',
    version='0.3',
    packages=find_packages(),
    include_package_data=True,
    license='GNU',
    description='Django admin chat',
    long_description=README,
    url='https://github.com/MrJackJones/django_admin_chat',
    author='Ivan Baranov',
    author_email='ibaranov1990@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2.6',
        'Intended Audience :: Developers',
        'License :: GNU License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
