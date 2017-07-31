clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

test:
	flake8
	nosetests

api:
	COUNTRY_PACKAGE=openfisca_country_template TRACKER_URL="https://openfisca.innocraft.cloud/piwik.php" TRACKER_IDSITE=1 gunicorn "openfisca_web_api_preview.app:create_app()" --bind localhost:5000 --workers 3
