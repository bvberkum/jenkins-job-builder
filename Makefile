T := \
	default install uninstall reinstall

.PHONY: $(T)

SHELL := /bin/bash
EMPTY :=
SPACE := $(EMPTY) $(EMPTY)

default:
	@echo "make [ $(subst $(SPACE), | ,$(T)) ]"

install::
	sudo python setup.py install

uninstall::
	sudo pip uninstall -y jenkins-job-builder
	pip uninstall -y jenkins-job-builder || printf ""
	pip uninstall -y jenkins-job-builder || printf ""

reinstall:: uninstall install
