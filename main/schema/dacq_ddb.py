from main.shared.shared import ma


class DacqSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'exp_id', 'fk_id', 'value', 'payment')


dacq_schema = DacqSchema()
dacqs_schema = DacqSchema(many=True)
