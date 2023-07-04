from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in justdial_email_integration/__init__.py
from justdial_email_integration import __version__ as version

setup(
	name="justdial_email_integration",
	version=version,
	description="This Integration will allow erpnext to get Lead from JusdDial using Email",
	author="New Indictrans Tech Pvt Ltd",
	author_email="contact@indictranstech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
