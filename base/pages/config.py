from flask import current_app


ROOT = current_app.config.get('PAGES_ROOT', 'p').strip('/')
TEMPLATE = current_app.config.get('PAGES_TEMPLATE', 'pages/page.html')
