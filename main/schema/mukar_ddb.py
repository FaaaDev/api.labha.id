from ..shared.shared import ma


class MukarSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "inc_id", "so_id", "t_bayar", "value", "remain", "desc")


mukar_schema = MukarSchema()
mukars_schema = MukarSchema(many=True)
