from flask import Blueprint, abort, redirect

from .config import ROOT
from .models import Page


pages = Blueprint('pages', __name__,
                  template_folder='templates',
                  static_url_path='/static/pages',
                  static_folder='static')


@pages.route('/%s/<path:pages>' % ROOT, methods=['GET'])
def page(pages):
    current_page = pages.strip('/').split('/')[-1]
    current_page = Page.query.filter_by(slug=current_page).first()

    if current_page is None:
        return abort(404)

    if current_page.link:
        return redirect(current_page.link)

    return current_page.render()
