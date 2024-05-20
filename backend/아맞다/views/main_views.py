from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def _init():
    return redirect(url_for('auth.login'))
    
@bp.route('/lost_main/')
def lost_main():
    return render_template('lost_found/main.html')