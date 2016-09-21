T := \
	default install uninstall reinstall

.PHONY: $(T)

SHELL := /bin/bash
EMPTY :=
SPACE := $(EMPTY) $(EMPTY)

default:
	@echo "make [ $(subst $(SPACE), | ,$(T)) ]"

install::
	pip install -r requirements.txt -e .

uninstall::
	pip uninstall -y jenkins-job-builder

reinstall:: uninstall install
