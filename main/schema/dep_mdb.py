from main.shared.shared import ma


class DepSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "cp_id", "name", "user_id")


dep_schema = DepSchema()
deps_schema = DepSchema(many=True)
