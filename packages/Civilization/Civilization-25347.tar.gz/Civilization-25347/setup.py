from setuptools import setup, find_packages
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name='Civilization',
    version=version,
    description='Civ',
    author='Dnet_n_Danya',
    author_email='demisrus5554@gmail.com',
    license='None',
    packages=find_packages(),
    url='https://gitlab.com/pypri/pypri-gitlab-ci',
    zip_safe=False
)