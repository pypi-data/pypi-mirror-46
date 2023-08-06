import setuptools

my_classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Topic :: Software Development :: Libraries :: Application Frameworks",
		"Topic :: Multimedia :: Graphics",
		"Operating System :: OS Independent",
]

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	description="PySimpleGUI designer, that uses transpiler to produce code from Qt Designer xml file.",
	entry_points={"console_scripts": ["PySimpleGUIDesigner = PySimpleGUIDesigner.main:cli"]},
	url="https://github.com/nngogol/PySimpleGUI_designer",
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	author_email="nngogol09@gmail.com",
	long_description=long_description,
	name="PySimpleGUIDesigner",
	author="Nikolay Gogol",
	license='GNU-GPL',
	version="0.0.1",
	classifiers=my_classifiers,
	package_data={'': ['*.ui']},
	install_requires=['PySide2', 'click>=7.0', 'PySimpleGUI'],
	#  _            _           _
	# (_)          | |         | |
	#  _ _ __   ___| |_   _  __| | ___
	# | | '_ \ / __| | | | |/ _` |/ _ \
	# | | | | | (__| | |_| | (_| |  __/
	# |_|_| |_|\___|_|\__,_|\__,_|\___|
)