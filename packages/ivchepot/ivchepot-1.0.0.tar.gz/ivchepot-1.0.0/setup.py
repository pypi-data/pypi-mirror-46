from setuptools import setup


def readme_file_contents():
	with open('README.rst') as readme_file:
		data = readme_file.read()
	return data


setup(
	name="ivchepot",
	version="1.0.0",
	description="Simple TCP Honeypot",
	long_description=readme_file_contents(),
	author="Ivche1337",
	author_email="ivchepro@gmail.com",
	licence="MIT",
	packages=["ivchepot"],
	zip_safe=False,
	install_requires=[]
)
