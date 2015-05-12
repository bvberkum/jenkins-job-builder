T := \
	default reinstall

.PHONY: $(T)

SHELL := /bin/bash

EMPTY :=
SPACE := $(EMPTY) $(EMPTY)

default:
	@echo "make [ $(subst $(SPACE), | ,$(T)) ]"

reinstall:
	sudo pip uninstall -y jenkins-job-builder
	sudo python setup.py install
