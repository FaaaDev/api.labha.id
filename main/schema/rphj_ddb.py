from main.shared.shared import ma


class RphjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "phj_id", "prod_id", "unit_id", "qty")


rphj_schema = RphjSchema()
rphjs_schema = RphjSchema(many=True)
