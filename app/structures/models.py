from app import db
from flask import url_for
import math


class SectionType(db.Model):
    __tablename__ = "section_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abb = db.Column(db.String, nullable=False, unique=True)
    parameters = db.Column(db.PickleType, nullable=False)

    def __init__(self, name, abb, parameters):
        self.name = name
        self.abb = abb
        self.parameters = parameters

    def __repr__(self):
        return '<SectionType %r' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'abb': self.abb,
            'parameters': self.parameters,
            '_links': {
                'sections': {
                    'internal': url_for('structures.get_sections_of_section_type', id=self.id),
                    'external': url_for('structures.get_sections_of_section_type', id=self.id, _external=True)
                }
            }
        }


class SectionBase:

    name = ''
    type = None

    # parameters
    parameters = ''

    # section properties
    area = 0.0

    def serialize(self):
        return {
            'name': self.name,
            'parameters': self.parameters,
            'area': self.area,
            '_links': {
                'type':
                    {
                        'internal': url_for('structures.get_section_type', id=self.type.id),
                        'external': url_for('structures.get_section_type', id=self.type.id, _external=True)
                    }
            }
        }

    @property
    def parameter_array(self):
        return [float(e.strip()) for e in self.parameters.split(',')]


class DefinedSection(SectionBase, db.Model):
    __tablename__ = "defined_sections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # section type
    type_id = db.Column(db.Integer, db.ForeignKey('section_types.id'))
    type = db.relationship('SectionType')

    # parameters
    parameters = db.Column(db.PickleType, nullable=False)

    # section properties
    area = db.Column(db.Float, default=0.0)

    def serialize(self):
        ret = super(DefinedSection, self).serialize()

        ret['id'] = self.id

        return ret


class CustomSection(SectionBase):

    def __init__(self, name, type, parameters):
        self.name = name
        self.type = type
        self.parameters = parameters

        engine = SectionPropertyEngine(self)
        engine.calculate()

    @property
    def area(self):
        return SectionPropertyEngine(self).calculate_area()


class SectionPropertyEngine:

    section = None

    def __init__(self, section):
        self.section = section

    def calculate(self):
        self.section.area = self.calculate_area()

    def calculate_area(self):

        if self.section.type.id == 1:
            b = float(self.section.parameters['b'])
            h = float(self.section.parameters['h'])
            return b * h

        elif self.section.type.id == 2:
            d = float(self.section.parameters['d'])
            return (math.pi * (d ** 2.0)) / 4.0


