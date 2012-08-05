ENVBIN=$(CURDIR)/.env/bin
PIP=$(ENVBIN)/pip
PYTHON=$(ENVBIN)/python
PYBABEL=$(ENVBIN)/pybabel
BABELDIR=$(CURDIR)/base/translations
CONFIG=base.config.develop

all: .env

.env: requirements.txt
	virtualenv --no-site-packages .env
	$(PIP) install -M -r requirements.txt


.PHONY: shell
shell: .env/ manage.py
	$(PYTHON) manage.py shell -c $(CONFIG)


.PHONY: run
run: .env/ manage.py
	$(PYTHON) manage.py runserver -c $(CONFIG)


.PHONY: db
db: .env/ manage.py
	$(PYTHON) manage.py create_db -c $(CONFIG)

.db: db

.PHONY: migrate
migrate: .env/ manage.py .db
	$(PYTHON) manage.py migrate run -c $(CONFIG)

.PHONY: test
test: .env/ manage.py
	nosetests

.PHONY: clean
clean:
	find $(CURDIR) -name "*.pyc" -delete
	find $(CURDIR) -name "*.orig" -delete

.PHONY: babel
babel: $(BABELDIR)/ru
	$(PYBABEL) extract -F $(BABELDIR)/babel.ini -k _gettext -k _ngettext -k lazy_gettext -o $(BABELDIR)/babel.pot --project Flask-base $(CURDIR)
	$(PYBABEL) update -i $(BABELDIR)/babel.pot -d $(BABELDIR)
	$(PYBABEL) compile -d $(BABELDIR)

$(BABELDIR)/ru:
	$(PYBABEL) init -i $(BABELDIR)/babel.pot -d $(BABELDIR) -l ru

.PHONY: chown
chown:
	sudo chown $(USER):$(USER) -R $(CURDIR)
