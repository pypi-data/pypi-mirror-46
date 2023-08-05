# nbunicorn

To push update to PyPi:

	python setup.py sdist
	twine upload dist/*

Validate push:
	
	pip install --upgrade nbunicorn
	pip freeze | grep nbunicorn