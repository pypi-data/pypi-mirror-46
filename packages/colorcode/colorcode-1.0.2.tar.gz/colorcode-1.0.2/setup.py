from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

import info

copt = {
	'msvc': ['/std:c++17', '/O2', '/permissive-'],
	'mingw32' : ['-std=c++17', '-O3', '-pedantic'],
	'cygwin' : ['-std=c++17', '-O3', '-pedantic'],
	'unix' : ['-std=c++17', '-O3', '-pedantic'],
}
lopt = {
}

class build_ext_subclass( build_ext ):
	def build_extensions(self):
		c = self.compiler.compiler_type
		if c in copt:
			for e in self.extensions:
				e.extra_compile_args = copt[ c ]
		if c in lopt:
			for e in self.extensions:
				e.extra_link_args = lopt[ c ]
		build_ext.build_extensions(self)

CYTHON_MODULES = [
	Extension(
		name = "colorcode.aztec.encoder",
		sources = [
			"colorcode/aztec/encoder/__init__.pyx",
			"colorcode/aztec/encoder/FixLenInteger.cpp",
			"colorcode/aztec/encoder/Constants.cpp",
			"colorcode/aztec/encoder/EncodingPath.cpp",
			"colorcode/aztec/encoder/Utility.cpp",
		],
		depends = [
			"colorcode/aztec/encoder/charmap.inc",
			"colorcode/aztec/encoder/Constants.h",
			"colorcode/aztec/encoder/EncodingPath.h",
			"colorcode/aztec/encoder/FixLenInteger.h",
			"colorcode/aztec/encoder/Mode.h",
			"colorcode/aztec/encoder/Utility.h",
		],
		language = "c++",
	),
	Extension(
		name = "colorcode.aztec.reedsolomon.galloisfield",
		sources = [
			"colorcode/aztec/reedsolomon/galloisfield.pyx",
		],
		language = "c",
	),
]

setup(
	name = "colorcode",
	version = info.VERSION,
	description = info.PROJECT_DESC,
	long_description = info.DESCRIPTION_TEXT,
	url = info.PROJECT_URL,
	author = info.AUTHOR_NAME,
	author_email = info.AUTHOR_EMAIL,

	packages = [
		"colorcode",
	],
	ext_modules = cythonize(CYTHON_MODULES),
	cmdclass = {'build_ext': build_ext_subclass },
	install_requires = [
		"Cython",
		"numpy",
		"Pillow"
	],
	zip_safe = False,
	classifiers=[
		'Development Status :: 7 - Inactive',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: C++',
		'Programming Language :: Cython',
		'Programming Language :: Python :: 3',
		'Topic :: Multimedia :: Graphics',
		'Topic :: Utilities',
	],
	entry_points = {
		'console_scripts' : [
			'colorcode=colorcode.cli:main',
		],
	},

)