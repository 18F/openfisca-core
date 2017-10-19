clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

test:
	flake8
	nosetests

api:
	openfisca-serve --country_package openfisca_country_template --extensions openfisca_extension_template
