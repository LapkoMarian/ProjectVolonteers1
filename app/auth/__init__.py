from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

auth_blueprint = Blueprint('auth', __name__, template_folder="templates")

from . import view
