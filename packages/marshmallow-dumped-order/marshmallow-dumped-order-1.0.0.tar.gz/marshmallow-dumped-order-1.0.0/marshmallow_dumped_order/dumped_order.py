from marshmallow import post_dump


def dumped_order(*fields_names):
    """Sort fields in needed order while dumping.

    Usage:

    .. code-block:: python

        from marshmallow import Schema, fields
        from marshmallow_dumped_order import dumped_order


        @dumped_order("name", "age")
        class User(Schema):
            age = fields.Int()
            name = fields.String()


        user_schema = User()
        dumped = user_schema.dumps({"age": 35, "name": "Jarvis"})

        assert dumped.data == '{"name": "Jarvis", "age": 35}'

    :param str fields_names: dumped fields names
    """

    def decorate(schema):
        class OrderedSchema(schema):
            @post_dump
            def right_ordering(self, data):
                return {
                    **{field_name: data.pop(field_name) for field_name in fields_names},
                    **data,
                }

        # Saving original schema's name is needed for some instruments
        # (for example for correct APISpec building with apispec library)
        OrderedSchema.__name__ = schema.__name__
        return OrderedSchema

    return decorate
