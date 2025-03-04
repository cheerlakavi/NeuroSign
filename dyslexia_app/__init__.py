from flask import Blueprint

dyslexia_bp = Blueprint('dyslexia', __name__, template_folder="templates")

from . import routes
