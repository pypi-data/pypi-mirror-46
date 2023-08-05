from setuptools import setup, find_packages

setup(
	name="pipshow",
	version="0.3",
	license="MIT",
	description="A script to show details of any python package, irrespective of whether its installed or not.",
	long_description="file: README.md",
	keywords="pip,setup,installer",
	url="https://github.com/prahladyeri/pipshow",
	packages=find_packages(),
	#scripts=['pipshow.py'],
	entry_points={
		"console_scripts": [
			"pipshow = pipshow.pipshow:main",
		],
	},
	install_requires=['requests'],
	# package_data = {
		# 'pipshow': ['./'],
	# },
	author="Prahlad Yeri",
	author_email="prahladyeri@yahoo.com",
	
)