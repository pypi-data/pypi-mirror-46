# -*- coding unix -*-

from cerberus import Validator
import lmrt4u.helpers as helpers

schema = {
        'sprints': {
            'type': 'dict',
            'valueschema': {
                'type': 'dict',
                'schema': {
                    'active': { 'type': 'boolean' },
                    'points': { 'type': 'integer' },
                    'start': { 'type': 'datetime', 'coerce': helpers.to_date, 'is_before': 'end' },
                    'end': { 'type': 'datetime', 'coerce': helpers.to_date },
                    'stories': { 'type': 'list', 'schema': {'type': 'list'} }
                }
            }
        }
}

class CustomValidator(Validator):
    """Allows for isBefore datetime validation"""
    def _validate_is_before(self, other, field, value):
        """ 
        Validate field is before other field.
        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        if other not in self.document:
            return False
        if value > self.document[other]:
            self._error(field, 
            "%s is an early date." % other)

def validate(rawData):
    """Validates file contents"""
    v = CustomValidator()
    return v.validate(rawData, schema)
