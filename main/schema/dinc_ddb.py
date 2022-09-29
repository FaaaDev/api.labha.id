from main.shared.shared import ma


class DincSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'inc_id', 'bnk_code', 'value', 'desc')


dinc_schema = DincSchema()
dincs_schema = DincSchema(many=True)
