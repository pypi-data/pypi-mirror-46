
import base64

from colibris.schemas import ValidationError
from colibris.schemas import fields

from testmyesp import instructions


class InstructionParamsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        instruction_class = instructions.get_instruction_class(obj['name'])
        if instruction_class is None:
            return ''

        schema_class = instruction_class.get_schema_class()
        schema = schema_class()

        return schema.dump(obj['params'])

    def _deserialize(self, value, attr, data, **kwargs):
        instruction_class = instructions.get_instruction_class(data['name'])
        if instruction_class is None:
            return None

        schema_class = instruction_class.get_schema_class()
        schema = schema_class()

        return schema.load(data['params'])


class Base64Field(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''

        return base64.b64encode(value).decode()

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return base64.b64decode(value)

        except Exception as e:
            raise ValidationError('Invalid base-64 value: {}.'.format(e))
