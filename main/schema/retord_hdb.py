from ..shared.shared import ma


class RetordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ret_code', 'ret_date', 'fk_id', 'inv_id')


retord_schema = RetordSchema()
retords_schema = RetordSchema(many=True)
