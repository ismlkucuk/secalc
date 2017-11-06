from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort
from app.structures.models import SectionType, DefinedSection, SectionPropertyEngine

from app import db

structures = Blueprint('structures', __name__, url_prefix='/structures')


@structures.route('/section_types', methods=['GET'])
def get_section_types():

    return jsonify([e.serialize() for e in SectionType.query.all()])

    return jsonify([
        {
            'id': e.id,
            'name': e.name,
            'abb': e.abb,
            '_links':
                {
                    'details': {
                        'internal': url_for('structures.get_section_type', id=e.id),
                        'external': url_for('structures.get_section_type', id=e.id, _external=True)
                    }
                }
        } for e in SectionType.query.all()
    ])


@structures.route('/section_types/<int:id>', methods=['GET'])
def get_section_type(id):

    section_type = SectionType.query.get(id)

    if section_type is None:
        abort(404)

    return jsonify(section_type.serialize())


@structures.route('/section_types/<int:id>/sections', methods=['GET'])
def get_sections_of_section_type(id):
    section_type = SectionType.query.get(id)

    if section_type is None:
        abort(404)
    sections = DefinedSection.query.filter(DefinedSection.type == section_type).all()

    return jsonify([
        {
        'id': e.id,
        'name': e.name,
        '_links': {
            'details': {
                'external': url_for('structures.get_section', id=e.id, _external=True),
                'internal': url_for('structures.get_section', id=e.id)
            }
        }
        } for e in sections
    ])


@structures.route('/sections', methods=['GET'])
def get_sections():
    sections = DefinedSection.query.all()

    return jsonify([
        {'id': e.id,
         'name': e.name,
         '_links':
            {
                'details': {
                    'internal': url_for('structures.get_section', id=e.id),
                    'external': url_for('structures.get_section', id=e.id, _external=True)
                }
            }
         } for e in sections
    ])


@structures.route('/sections/<int:id>', methods=['GET'])
def get_section(id):
    section = DefinedSection.query.get(id)

    if section is None:
        abort(404)

    return jsonify(section.serialize())


@structures.route('/custom_section', methods=['POST'])
def get_custom_section():

    data = request.get_json(silent=True)

    id = data.get('id', None)
    name = data.get('name', None)
    type_abb = data.get('type_abb', None)
    type_id = data.get('type_id', None)
    parameters = data.get('parameters', None)

    if type_id is not None:
        type = SectionType.query.get(type_id)
    else:
        type = SectionType.query.filter(SectionType.abb  == type_abb).one()

    if type is None:
        abort(404)

    sec = DefinedSection()
    sec.id = id
    sec.name = name
    sec.type = type
    sec.parameters = parameters

    engine = SectionPropertyEngine(sec)
    engine.calculate()

    if sec.id is None:
        db.session.add(sec)
        db.session.commit()
    else:
        db.session.merge(sec)
        db.session.commit()

    return jsonify(sec.serialize())