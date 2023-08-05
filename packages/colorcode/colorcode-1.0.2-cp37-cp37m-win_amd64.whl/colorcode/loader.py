
"""
Load code builder modules

This module loads (imports) other code builder modules.

These modules have to be in the same directory.

Attributes
----------
EXCLUDE_MODULES : :py:class:`list`
	A list of string containing the name of modules that must be ignored,
	because they are not code builder modules
BUILDERS : :py:class:`dict`
	A dictionnary containg found modules. The keys of this dictionnary
	are the module names, the values are builder descriptions dictionnaries
	as defined in the next section.

Builder descriptions
--------------------
	A "builder description dictionnary" is a dictionnary containing the following 5 entries:
	
	- ``id`` : The name of the module
	- ``name`` : The name of the code as defined in the builder module
	- ``builder`` : The code builder class
	- ``params`` : The set of parameters sent to the image builder
	- ``module`` : The builder module as it has been imported by Python

"""

import os
import sys
import importlib

EXCLUDE_MODULES = [
	"imgen",
	"loader.py",
	"cli.py",
]

def _findModules(location = '.'):
	exts = [
		'.py',
		'.pyd' if sys.platform.startswith('win') else '.so',
	]
	elements = os.scandir(location)
	for item in elements:
		if item.name.startswith('_') or item.name in EXCLUDE_MODULES:
			continue
		if item.is_file() and not any(item.name.endswith(i) for i in exts):
			continue
		if item.is_dir() and not os.access(os.path.join(item.path, '__init__.py'), os.R_OK):
			continue
		filename = os.path.splitext(item.name)[0]
		if '.' in filename:
			continue
		yield filename

def _findBuilders(location = '.'):
	for modname in _findModules(location):
		if __name__ == '__main__':
			module = importlib.import_module(modname)
		else:
			module = importlib.import_module('.' + modname, '.'.join(__name__.split('.')[:-1]))
		try:
			builder = module.Builder
			params = module.IMGEN_PARAMS
			name = module.NAME
		except AttributeError:
			continue
		yield {
			'id' : modname,
			'name' : name,
			'builder' : builder,
			'params' : params,
			'module' : module,
		}

BUILDERS = {mod['id'] : mod for mod in _findBuilders(os.path.dirname(__file__))}

def listBuilders():
	"""
	Generates a list of builder modules found

	This metod generates a read-to-print list
	of code builder modules found.
	Each module is a line in the returned string, in the form:
	``{module name} : {code name} <{builder class}>``

	Returns
	-------
	:py:class:`str`
		A single mutli-line string containing the list
		of installed code generator modules
	"""
	return '\n'.join("{0[id]} : {0[name]} {0[builder]!r}".format(m) for m in BUILDERS.values())
