from ..shared.shared import ma


class MukapSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "exp_id", "po_id", "t_bayar", "value", "remain", "desc")


mukap_schema = MukapSchema()
mukaps_schema = MukapSchema(many=True)
