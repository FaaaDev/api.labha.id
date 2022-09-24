from main.shared.shared import ma


class NeracaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "cp_id", "cur", "fixed", "depr", "ap", "cap", "user_id")


neraca_schema = NeracaSchema()
neracas_schema = NeracaSchema(many=True)
