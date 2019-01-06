#red:=$(shell tput setaf 1)
#reset:=$(shell tput sgr0)

init:
	pip install -r requirements.txt

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf arlo.egg-info

commit:
	test -n "$(message)" || $(error "Error: commit message required. Usage: make $(MAKECMDGOALS) message='<your commit message here>'")
	python rev.py 
	git add setup.py
	git commit -m "$(message)"
	git push

release: clean commit
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --skip-existing dist/*
