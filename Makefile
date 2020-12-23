REQUIREMENTS		:= requirements.txt
PIP					:= pip

.PHONY: all dep push


all: dep push


dep: $(REQUIREMENTS)
	$(PIP) install -r $<


add:
	git add -A

commit: add .git
	# Not Recommended
	git commit -m 'Update project'


push: commit
	git push
