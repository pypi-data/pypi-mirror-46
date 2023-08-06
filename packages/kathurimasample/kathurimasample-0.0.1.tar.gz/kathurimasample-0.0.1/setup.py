from setuptools import setup

def readme():
	with open('README.md') as f:
		README = f.read()
		return README

setup(
		name = "kathurimasample",
		version="0.0.1",
		description="Kathurima sample package Python project",
		long_description=readme(),
		long_description_content_type="text/markdown",
		url="https://github.com/KathurimaKimathi/pythonproject",
		author="Kathurima Kimathi", 
		author_email="kathurimakimathi@gmail.com",
		license="MIT",

		classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        #'Intended Audience :: Developers',
        #'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        #'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
],

		packages=["myfibo"], 
		include_package_data=True,
		install_requires=["requests"],
		entry_points={
			"console_scripts": [
				"packagemanagement=myfibo.fibo:recur_fibo",
			]
		},

	)