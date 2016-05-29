T := \
	default install uninstall reinstall

.PHONY: $(T)

default::

install::
	python setup.py install

uninstall::
	pip uninstall -y jenkins-job-builder

reinstall:: uninstall install
