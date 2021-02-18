#########################################################################
#																		#
#                     Project management utilities                     	#
#		      		  ----------------------------						#
#																		#
#########################################################################

define PROJECT_HELP_MSG

Usage:\n
	\n
    make help\t\t\t             show this message\n
	\n
	-------------------------------------------------------------------------\n
	\t\tInstallation and start/stop the server\n
	-------------------------------------------------------------------------\n
	make\t\t\t\t                Install lisacattools in the system (root)\n
	make user\t\t\t 			Install lisacattools for non-root usage\n
	\n
	-------------------------------------------------------------------------\n
	\t\tDevelopment\n
	-------------------------------------------------------------------------\n
	make prepare-dev\t\t 		Prepare Development environment\n
	make install-dev\t\t 		Install COTS\n
	make install-demo\t\t           Install demo\n
	make test\t\t\t             Run units and integration tests\n
	\n\t\t\t\t 					(run make server-test before)
	\n
	make demo\t\t\				Play the demo
	make doc\t\t\t 				Generate the documentation\n
	make visu-doc\t\t\t			View the generated documentation\n
	make release\t\t\t 			Release the package\n
	\n
	-------------------------------------------------------------------------\n
	\t\tOthers\n
	-------------------------------------------------------------------------\n
	make licences\t\t	Display the list of licences



endef
export PROJECT_HELP_MSG

VENV = ".lisacattools-env"

#
# Sotware Installation in the system (need root access)
# -----------------------------------------------------
#
init:
	python3 setup.py install

#
# Sotware Installation for user
# -----------------------------
# This scheme is designed to be the most convenient solution for users
# that don’t have write permission to the global site-packages directory or
# don’t want to install into it.
#
user:
	python3 setup.py install --user

#Show help
#---------
help:
	echo $$PROJECT_HELP_MSG

#
# Development - prepare env
# ----------------------------------
#
prepare-dev:
	echo "python3 -m venv lisacattools-env && export PYTHONPATH=." > .lisacattools-env && echo "source \"`pwd`/lisacattools-env/bin/activate\"" >> .lisacattools-env && scripts/install-hooks.bash && echo "\nnow source this file: \033[31msource ${VENV}\033[0m"

install-dev:
	pip install -r requirements.txt && pip install -r requirements-dev.txt

install-demo:
	pip install -r requirements-demo.txt && echo "please download https://drive.google.com/u/0/uc?export=download&id=1iL071Fi5MxHle0CLOqg3JkZIgjQF8EwF , untar the file to tutorial/data"
#
# Development - create doc and tests
# ----------------------------------
#
doc:
	make html -C docs

visu-doc:
	firefox docs/build/html/index.html

test:
	scripts/run-tests.bash

#
# Create distribution
# ----------------------------------
#
changelog:
	gitchangelog > CHANGELOG

clean:
	rm -rf dist/ build/ lisacattools.egg-info/ && make clean -C docs && find ./lisacattools -name '*.pyc' | xargs rm

release:
	make clean && make changelog && python3 setup.py sdist && make doc

demo:
	./lisacattools-env/bin/jupyter-notebook tutorial/MBHdemo.ipynb

licences:
	pip-licenses

.PHONY: help user prepare-dev install-dev doc visu-doc test changelog clean release licences
