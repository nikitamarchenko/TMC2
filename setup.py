from setuptools import setup, find_packages
from pip.req import parse_requirements


install_requires_pip = parse_requirements('requirements.txt')

install_requires_setuptools = []
dependency_links_setuptools = []

for ir in install_requires_pip:
    if ir.url and ir.url.startswith('git'):
        dependency_links_setuptools.append(ir.url)
    install_requires_setuptools.append(str(ir.req))

setup(
    name='tmc',
    version='2',
    packages=find_packages(),
    url='',
    license='',
    author='nmarchenko',
    author_email='',
    description='',
    setup_requires=["setuptools_git >= 0.3", ],
    entry_points={
        'console_scripts': [
        ]
    },
    install_requires=install_requires_setuptools,
    dependency_links=dependency_links_setuptools,
    include_package_data=True
)
