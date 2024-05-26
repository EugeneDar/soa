from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(load_only=True, required=True)
    password = fields.Str(load_only=True, required=True)
    name = fields.Str()
    surname = fields.Str()
    birthdate = fields.Date()
    email = fields.Str()
    phone = fields.Str()
