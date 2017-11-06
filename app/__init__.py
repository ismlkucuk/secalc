# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 404,
                    'message': 'page not found',
                    'requested_url': request.url})

from app.structures.models   import DefinedSection, SectionType

@app.route('/', methods=['GET'])
def index():
    return render_template('main_template.html')

# Import a module / component using its blueprint handler variable (mod_auth)
from app.structures.controllers import structures as structures_module

# Register blueprint(s)
app.register_blueprint(structures_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()