from setuptools import setup, find_packages

import adminplus

setup(
    name='django-adminplus',
    version=adminplus.__version__,
    description='Add new pages to the Django admin.',
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='me@jamessocol.com',
    url='http://github.com/jsocol/django-adminplus',
    license='BSD',
    packages=find_packages(exclude=['test_settings', 'test_urlconf']),
    include_package_data=True,
    package_data = {'': ['README.rst', 'templates/adminplus/*.html']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
