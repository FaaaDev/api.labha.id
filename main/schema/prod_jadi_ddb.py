from main.shared.shared import ma


class PJadiSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pp_id", "prod_id", "unit_id", "loc_id", "qty")


prod_jadi_schema = PJadiSchema()
prod_jadis_schema = PJadiSchema(many=True)
