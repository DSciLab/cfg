REQUIREMENTS   := requirements.txt
PIP            := pip
PYTHON         := python


.PHONY: all dep install clean dist build


all: dep install


dist: clean
	$(PYTHON) setup.py sdist


build: dist


dep: $(REQUIREMENTS)
	$(PIP) install -r $<


install: dep
	$(PYTHON) setup.py install


clean:
<<<<<<< HEAD
	-rm -rf .eggs .tox build MANIFEST dist
=======
	-rm -rf dist .eggs .tox build MANIFEST
>>>>>>> nf
