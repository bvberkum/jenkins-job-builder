T := \
	default install uninstall reinstall

.PHONY: $(T)

SHELL := /bin/bash

EMPTY :=
SPACE := $(EMPTY) $(EMPTY)

default:
	@echo "make [ $(subst $(SPACE), | ,$(T)) ]"

install::
	sudo -H python setup.py install

uninstall::
	sudo -H pip uninstall -y jenkins-job-builder

reinstall:: uninstall install
