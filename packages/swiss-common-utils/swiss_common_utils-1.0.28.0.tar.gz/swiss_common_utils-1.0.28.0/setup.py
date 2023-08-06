from setuptools import setup, find_packages

from install_requirements import get_required_packages
from version import get_package_version

setup(
    name='swiss_common_utils',
    version=get_package_version(),
    packages=find_packages(),
    url='',
    license='',
    author='lior.yehonatan',
    author_email='lior.yehonatan@inel.com',
    description='swiss common utils',
    python_requires='>=3.6',
    install_requires=get_required_packages()
)
