SHELL := /bin/bash

.PHONY : help init config bucket deploy test clean delete
.DEFAULT: help

VENV_NAME ?= venv
PYTHON ?= $(VENV_NAME)/bin/python
AWS_CLI = $(VENV_NAME)/bin/aws
GENERATE_ID ?= $(shell dd if=/dev/random bs=8 count=1 2>/dev/null | od -An -tx1 | tr -d ' \t\n')
SET_ID = $(eval BUCKET_ID=$(GENERATE_ID))
BUCKET_NAME = $(shell basename $(PWD)-$(BUCKET_ID))
STACK_NAME = $(shell basename $(PWD))
CONFIG_FILE = config.mk
LAYER_PATH ?= ./src/layers

ifneq ("$(wildcard $(CONFIG_FILE))","")
	include $(CONFIG_FILE)
endif

help:
	@echo "init	create VirtualEnv and install libraries"
	@echo "config	create configuration file"
	@echo "bucket	create S3 bucket"
	@echo "deploy	deploy CloudFormation stacks"
	@echo "test	run pre-commit checks"
	@echo "clean	delete VirtualEnv and installed libraries"
	@echo "delete	delete CloudFormation stacks"

# Install VirtualEnv and dependencies
init: $(VENV_NAME)
	make pre-commit

$(VENV_NAME): $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -Ur requirements.txt
	touch $(VENV_NAME)/bin/activate

pre-commit:
	. $(VENV_NAME)/bin/activate && pre-commit install

# Cleanup VirtualEnv
clean:
	rm -rf venv
	find . -iname "*.pyc" -delete

# Generate configuration file
config:
ifneq ("$(wildcard $(CONFIG_FILE))","")
	@echo "File $(CONFIG_FILE) exists. Abort"
else
	@touch config.mk
	@read -p "AWS Region to create bucket in (e.g. us-east-1)?: " REGION && echo AWS_REGION=$$REGION >> $(CONFIG_FILE);
	$(SET_ID)
	@echo BUCKET_NAME=$(BUCKET_NAME) >> $(CONFIG_FILE)
	@echo STACK_NAME=$(STACK_NAME) >> $(CONFIG_FILE)
	@echo "Configuration written to $(CONFIG_FILE) file."
endif

# Create S3 bucket
bucket:
	@$(AWS_CLI) s3 mb s3://$(BUCKET_NAME) \
	--region $(AWS_REGION)

# Build, Package, Deploy and Destroy
build:
	@for layer in $(LAYER_PATH)/*; do \
  		printf "\n--> Installing %s requirements...\n" $${layer}; \
		pip install -r $${layer}/requirements.txt --target $${layer}/python --upgrade; \
	done

package: build
	@printf "\n--> Packaging and uploading templates to the %s S3 bucket ...\n" $(BUCKET_NAME)
	@aws cloudformation package \
  	--template-file ./cfn/main.template \
  	--s3-bucket $(BUCKET_NAME) \
  	--s3-prefix $(STACK_NAME) \
  	--output-template-file ./cfn/packaged.template \
  	--region $(AWS_REGION)

deploy: package
	@printf "\n--> Deploying %s template...\n" $(STACK_NAME)
	@aws cloudformation deploy \
	  --template-file ./cfn/packaged.template \
	  --stack-name $(STACK_NAME) \
	  --region $(AWS_REGION) \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
	  --parameter-overrides \
	  	LambdaRuntimeEnv=$(LAMBDA_RUNTIME_ENV)

delete:
	@printf "\n--> Deleting %s stack...\n" $(STACK_NAME)
	@aws cloudformation delete-stack \
            --stack-name $(STACK_NAME)
	@printf "\n--> $(STACK_NAME) deletion has been submitted, check AWS CloudFormation Console for an update..."

# Tests
test:
	$(VENV_NAME)/bin/pre-commit run --all-files

test-cfn-lint:
	cfn-lint cfn/*.template

test-cfn-nag:
	cfn_nag_scan --input-path cfn

# cfn-publish specific
cfn-publish-package: build
	zip -r packaged.zip -@ < ci/include.lst

version:
	@bumpversion --dry-run --list cfn/main.template | grep current_version | sed s/'^.*='//
