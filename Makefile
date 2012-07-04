PIP=$(CURDIR)/.env/bin/pip
PYTHON=$(CURDIR)/.env/bin/python
PYBABEL=$(CURDIR)/.env/bin/pybabel

all: .env

.env: requirements.txt
	virtualenv --no-site-packages .env
	$(PIP) install -M -r requirements.txt


.PHONY: shell
shell: .env/ manage.py
	$(PYTHON) manage.py shell


.PHONY: run
run: .env/ manage.py
	$(PYTHON) manage.py runserver


.PHONY: db
db: .env/ manage.py
	$(PYTHON) manage.py createall


.PHONY: test
test: .env/ manage.py
	nosetests

.PHONY: clean
clean:
	find $(CURDIR) -name "*.pyc" -delete
	find $(CURDIR) -name "*.orig" -delete

.PHONY: babel-init
babel-init:
	sh src/babel.sh

.PHONY: babel
babel: src/translations/
	$(PYBABEL) extract -F babel/babel.ini -k _gettext -k _ngettext -k lazy_gettext -o babel/babel.pot --project Flask-base src
	$(PYBABEL) update -i babel/babel.pot -d src/translations
	$(PYBABEL) compile -d src/translations

src/translations/:
	$(PYBABEL) init -i babel/babel.pot -d src/translations -l ru
