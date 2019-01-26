#red:=$(shell tput setaf 1)
#reset:=$(shell tput sgr0)

init:
	pip install -r requirements.txt

clean:
	rm -rf *.pyc
	rm -rf dist
	rm -rf build
	rm -rf __pycache__
	rm -rf arlo.egg-info

doc:
	#pydoc -w ../arlo/arlo.py
	#mv arlo.html arlo_api_doc.md
	#git add arlo_api_doc.md
	pdoc --overwrite --html --html-dir docs arlo.py
	sed -i'.bak' 's/#sidebar{width:30%}#content{width:70%;/#sidebar{width:45%}#content{width:55%;/g' docs/arlo.html
	rm docs/arlo.html.bak
	cp docs/arlo.html docs/README.md
	git add docs/*

rev:
	python rev.py
	git add setup.py

commit:
ifndef message
	$(error "Error: commit message required. Usage: make $(MAKECMDGOALS) message='<your commit message here>'")
endif

	git add Makefile

	git add arlo.py
	git add request.py
	git add eventstream.py

	git commit -m "$(message)"
	git push

release: clean rev doc commit
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload --skip-existing dist/*
