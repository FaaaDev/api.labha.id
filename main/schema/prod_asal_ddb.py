from main.shared.shared import ma


class PAsalSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pp_id", "prod_id", "unit_id", "loc_id", "qty")


prod_asal_schema = PAsalSchema()
prod_asals_schema = PAsalSchema(many=True)
