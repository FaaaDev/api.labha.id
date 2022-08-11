from main.shared.shared import ma


class PpbbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pbb_id", "prod_id", "unit_id", "qty")


ppbb_schema = PpbbSchema()
ppbbs_schema = PpbbSchema(many=True)
