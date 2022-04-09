## -----------------------------------------------------------------------------
## The purpose of this Makefile is to provide the commands to setup the
## environment for development of the todoist-extractor Project
## -----------------------------------------------------------------------------

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "};  \
	{printf "%-15s %s\n", $$1, $$2}'

miniconda:	## Downloads and install latest Miniconda3 x86_64 for Linux
	wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash Miniconda3-latest-Linux-x86_64.sh -p ~/miniconda
	rm Miniconda3-latest-Linux-x86_64.sh

env-create-todoist:	## Creates a conda environment named "bases" with Python 3.8
	conda create -n todoist python=3.10 --yes

env-remove-todoist:	## Removes the "bases" environment
	conda env remove -n todoist

# must run `conda activate bases` before executing this
env-setup-todoist:  ## Sets up the environment for development
	# Install repository as an editable package
	pip install -r requirements.txt


	# Install jupyter to remove notebooks output
	pip install jupyter
env-java-install: ## Install Java in enviroment
	sudo apt install openjdk-11-jdk

env-import-todoist:
	pip install -e ./