from marshmallow import (
    Schema,
    fields,
    validate,
)


class CrossRefResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    doi = fields.String(required=True, validate=not_blank)
    authors = fields.String()
    doi_url = fields.String()
    issn = fields.String()
    issue = fields.String()
    journal = fields.String()
    pages = fields.String()
    pmid = fields.String()
    ref_type = fields.String()
    text = fields.String()
    title = fields.String()
    volume = fields.String()
    year = fields.Integer()
    updated_at = fields.DateTime(dump_only=True)


class CrossRefQueryParamsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer()
    doi = fields.String(validate=not_blank)
