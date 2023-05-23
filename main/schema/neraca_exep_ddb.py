from ..shared.shared import ma


class NeracaExepSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "tittle_id", "accounts", "user_id", )


neracaExep_schema = NeracaExepSchema()
neracaExeps_schema = NeracaExepSchema(many=True)
