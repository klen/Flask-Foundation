PIP=$(CURDIR)/.env/bin/pip
PYTHON=$(CURDIR)/.env/bin/python

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

