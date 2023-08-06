''' Setup for package '''
from setuptools import setup, find_packages

setup(
    name='crackle-automation-api-client',
    version='0.2',
    description="Python API Wrapper for Crackle Automation Reporter Web Service",
    long_description=""" """,
    classifiers=[],
    keywords='',
    author='Clark Mckenzie',
    author_email='clarkmckenzie@gmail.com',
    url='',
    license='No License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        "requests"
    ],
)
