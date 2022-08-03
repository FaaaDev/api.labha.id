from main.shared.shared import ma


class PphjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "phj_id", "prod_id", "unit_id", "qty")


pphj_schema = PphjSchema()
pphjs_schema = PphjSchema(many=True)
