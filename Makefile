init:
	pip install -r requirements.txt

upload:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload --skip-existing dist/*

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf arlo.egg-info

