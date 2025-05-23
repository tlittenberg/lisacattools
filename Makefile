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
	make data\t\t\t				Download data\n
	make test\t\t\t             Run units and integration tests\n
	make quality\t\t\t 			Run quality tests\n
	make tox\t\t\t 			Tests in several environments\n

	\n
	make demo\t\t\t				Play the demo\n
	make doc\t\t\t 				Generate the documentation\n
	make doc-pdf\t\t\t 			Generate the documentation as PDF\n
	make visu-doc-pdf\t\t 		View the generated PDF\n
	make visu-doc\t\t\t			View the generated documentation\n
	\n
	make clean\t\t\t		Clean .pyc files, __pycache__ directories and documentation\n	
	make add_req_prod pkg=<name>\t Add the package in the dependencies of .toml\n
	make add_req_dev pkg=<name>\t Add the package in the DEV dependencies of .toml\n	
	make conda\t\t\t			Make conda package from Pypi\n
	make release-pypi\t\t   	Release the package for pypi\n
	make upload-test-pypi\t\t   Upload the pypi package on the test platform\n
	make upload-prod-pypi\t\t   Upload the pypi package on the prod platform\n
	\n
	-------------------------------------------------------------------------\n
	\t\tVersion\n
	-------------------------------------------------------------------------\n	
	make version\t\t\t		Display the version\n
	make add_major_version\t\t	Add a major version\n
	make add_minor_version\t\t	Add a minor version\n
	make add_patch_version\t\t	Add a patch version\n
	make add_premajor_version\t	Add a pre-major version\n
	make add_preminor_version\t	Add a pre-minor version\n
	make add_prepatch_version\t	Add a pre-patch version\n
	make add_prerelease_version\t	Add a pre-release version\n
	\n	
	-------------------------------------------------------------------------\n
	\t\tRelease\n
	-------------------------------------------------------------------------\n
	make release\t\t\t 			Release the package as tar.gz\n
	make release-pypi\t\t		Prepare pypi release\n
	make upload-test-pypi\t\t	Upload the release on test.pypi.org\n
	make upload-prod-pypi\t\t	Upload the release on pypi.org\n	
	\n
	-------------------------------------------------------------------------\n
	\t\tMaintenance (use make install-dev before using these tasks)\n
	-------------------------------------------------------------------------\n	
	make check_update\t\t 		Check the COTS update\n
	make update_req\t\t			Update the version of the packages in the authorized range in toml file\n
	make update_latest_dev\t\t	Update to the latest version for development\n
	make update_latest_main\t 	Update to the latest version for production\n
	make show_deps_main\t\t 	Show main COTS for production\n
	make show_deps_dev\t\t 		Show main COTS for development\n
	make show_obsolete\t\t		Show obsolete COTS\n
	\n	
	-------------------------------------------------------------------------\n
	\t\tOthers\n
	-------------------------------------------------------------------------\n
	make licences\t\t\t	Display the list of licences\n
	make tox\t\t\t 			Run all tests on supported env\n


endef
export PROJECT_HELP_MSG

VENV = ".venv"
VENV_RUN = ".lisacattools"

#
# Sotware Installation in the system (need root access)
# -----------------------------------------------------
#
init:
	@poetry install --only=main

#
# Sotware Installation for user
# -----------------------------
# This scheme is designed to be the most convenient solution for users
# that don’t have write permission to the global site-packages directory or
# don’t want to install into it.
#
user:
	@poetry install --no-root --user

#Show help
#---------
help:
	@echo $$PROJECT_HELP_MSG

#
# Development - prepare env
# ----------------------------------
#
prepare-dev:
	git config --global init.defaultBranch main
	git init
	echo "echo \"Using Virtual env for lisacattools.\"" > ${VENV_RUN}
	echo "echo \"Please, type 'deactivate' to exit this virtual env.\"" >> ${VENV_RUN}
	echo "python3 -m venv --prompt lisacattools ${VENV} && \
	export PYTHONPATH=. && \
	export PATH=`pwd`/${VENV}/bin:${PATH}" >> ${VENV_RUN} && \
	echo "source \"`pwd`/${VENV}/bin/activate\"" >> ${VENV_RUN} && \
	scripts/install-hooks.bash && \
	echo "\nnow source this file: \033[31msource ${VENV_RUN}\033[0m"

install-dev:
	@poetry install && poetry run pre-commit install && poetry run pre-commit autoupdate
	@poetry run python -m ipykernel install --user --name=${VENV}

data:
	@poetry install --only data && poetry run python scripts/data_download.py

version:
	@poetry version -s

add_major_version:
	@poetry version major
	@poetry lock
	@poetry run git tag `poetry version -s`

add_minor_version:
	@poetry version minor
	@poetry lock
	@poetry run git tag `poetry version -s`

add_patch_version:
	@poetry version patch
	@poetry lock
	@poetry run git tag `poetry version -s`

add_premajor_version:
	@poetry version premajor
	@poetry lock

add_preminor_version:
	@poetry version preminor
	@poetry lock

add_prepatch_version:
	@poetry version prepatch
	@poetry lock

add_prerelease_version:
	@poetry version prerelease
	@poetry lock

add_req_prod:
	@poetry add "$(pkg)"

add_req_dev:
	@poetry add -G dev "$(pkg)"

check_update:
	@poetry show -l

update_req:
	@poetry update

update_latest_main:
	packages=$$(poetry show -T --only=main | grep -oP "^\S+"); \
	packages_latest=$$(echo $$packages | tr '\n' ' ' | sed 's/ /@latest /g'); \
	@poetry add -G main $$packages_latest

update_latest_dev:
	packages=$$(poetry show -T --only=dev | grep -oP "^\S+"); \
	packages_latest=$$(echo $$packages | tr '\n' ' ' | sed 's/ /@latest /g'); \
	@poetry add -G dev $$packages_latest

show_deps_main:
	@poetry show -T --only=main

show_deps_dev:
	@poetry show -T --only=dev

show_deps_data:
	@poetry show -T --only=data	

show_deps_demo:
	@poetry show -T --only=demo

show_deps_release:
	@poetry show -T --only=release			

show_obsolete:
	@poetry show -o


#
# Development - create doc and tests
# ----------------------------------
#
doc:
	make test
	cp tests/results/*.html docs/source/_static/
	cp -r tests/results/coverage docs/source/_static/
	make html -C docs

doc-pdf:
	make doc
	make latexpdf -C docs

visu-doc-pdf:
	@poetry run acroread docs/build/latex/lisacattools.pdf

visu-doc:
	@poetry run firefox docs/build/html/index.html

test:
	make data
	@poetry run scripts/run-tests.bash

quality:
	pre-commit run --all-files

tox:
	@command -v pyenv >/dev/null || { echo "❌ pyenv is not installed"; exit 1; }
	@pyenv versions --bare | grep -q '^3.10' || { echo "❌ Python 3.10 is not installed with pyenv"; exit 1; }
	@pyenv versions --bare | grep -q '^3.11' || { echo "❌ Python 3.11 is not installed with pyenv"; exit 1; }
	@pyenv versions --bare | grep -q '^3.12' || { echo "❌ Python 3.12 is not installed with pyenv"; exit 1; }
	@pyenv local 3.10 3.11 3.12
	@tox

#
# Create distribution
# ----------------------------------
#
changelog:
	@poetry install --only=release
	gitchangelog > CHANGELOG

clean:
	rm -rf dist/ build/ lisacattools.egg-info/ docs/source/examples_*
	make clean -C docs && find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

release:
	make clean
	make changelog
	@poetry build

conda:
	@poetry run bash scripts/to_conda.bash

release-pypi:
	make clean
	make changelog
	@poetry build
	@poetry run ${VENV}/bin/twine check dist/*

upload-test-pypi:
	@poetry run ${VENV}/bin/twine check dist/*
	@poetry run ${VENV}/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload-prod-pypi:
	@poetry run ${VENV}/bin/twine check dist/*
	@poetry run ${VENV}/bin/twine upload --repository-url https://pypi.org/legacy/ dist/*

demo:
	make data
	@poetry install --only=demo
	@poetry run ${VENV}/bin/jupyter-notebook tutorial/MBHdemo.ipynb

licences:
	@poetry run python3 scripts/license.py

.PHONY: show_obsolete show_deps_release show_deps_main show_deps_dev show_deps_data show_deps_demo update_latest_main update_latest_dev update_req check_update add_req_prod add_req_dev add_major_version add_minor_version add_patch_version add_premajor_version add_preminor_version add_prepatch_version add_prerelease_version help user prepare-dev install-dev data version doc visu-doc test tox changelog clean release release-pypi upload-test-pypi upload-prod-pypi demo licences conda
