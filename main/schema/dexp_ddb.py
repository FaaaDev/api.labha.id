from main.shared.shared import ma


class DexpSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'exp_id', 'acc_code', 'value', 'desc')


dexp_schema = DexpSchema()
dexps_schema = DexpSchema(many=True)
