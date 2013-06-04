
MODULE=bctree

# Change this if you want this virtualenv to live alongside your other
# environments. If you do, be careful of the clean command which deletes the
# virtual environment.
VIRTUAL_ENV=/tmp/$(MODULE)-dev
PYTHON = $(VIRTUAL_ENV)/bin/python
SED=sed
PYLINT=pylint
PYLINTRC_SRC = $(PWD)/dev/etc/pylintrc
PYLINTRC = $(VIRTUAL_ENV)/bin/pylintrc

.PHONY: all clean virtualenv build test

all: virtualenv build pylint tests

virtualenv: $(VIRTUAL_ENV)

$(VIRTUAL_ENV):
	virtualenv $(VIRTUAL_ENV)

build: virtualenv
	$(PYTHON) setup.py develop

sdist: virtualenv
	$(PYTHON) setup.py sdist

bdist: virtualenv
	$(PYTHON) setup.py bdist

$(PYLINTRC): $(PYLINTRC_SRC)
	$(SED) "s%##REPLACE##%$(VIRTUAL_ENV)%" "$(PYLINTRC_SRC)" >| "$(PYLINTRC)"

pylint: build $(PYLINTRC)
	$(PYLINT) --rcfile="$(PYLINTRC)" $(MODULE)

clean:
	rm -rf $(VIRTUAL_ENV) build dist *.egg-info log

dist-clean: clean

tests: build
	$(PYTHON) -m unittest discover -v -s $(MODULE)/tests
