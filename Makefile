REQUIREMENTS		:= requirements.txt
PIP					:= pip

.PHONY: all dep push


all: dep push


dep: $(REQUIREMENTS)
	$(PIP) install -r $<


commit:
	# Not Recommended
	git add -A
	git commit -m 'Update project'


push: commit
	git push
