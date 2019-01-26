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

docs:
	pydoc -w ../arlo/arlo.py
	git add arlo.html

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

release: clean rev docs commit
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload --skip-existing dist/*
