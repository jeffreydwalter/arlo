init:
	pip install -r requirements.txt

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf arlo.egg-info

commit:
	python rev.py 
	git add setup.py
	git commit -m "$(msg)"

release: commit
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --skip-existing dist/*
