from main.shared.shared import ma


class RetordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ret_code', 'ret_data', 'fk_id')


retord_schema = RetordSchema()
retords_schema = RetordSchema(many=True)
