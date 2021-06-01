REQUIREMENTS   := requirements.txt
PIP            := pip
PYTHON         := python


.PHONY: all dep push install clean dist


all: dep push install build


dist: clean
	$(PYTHON) setup.py sdist


build: dist


dep: $(REQUIREMENTS)
	$(PIP) install -r $<


install: dep
	$(PYTHON) setup.py install


clean:
	-rm -rf .eggs .tox build MANIFEST dist
