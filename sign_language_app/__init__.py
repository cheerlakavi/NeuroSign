from flask import Blueprint

sign_language_bp = Blueprint('sign_language', __name__, template_folder="templates")

from . import routes
