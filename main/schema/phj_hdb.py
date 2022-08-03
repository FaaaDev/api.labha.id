from main.shared.shared import ma


class PhjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "phj_code", "phj_date", "batch_id")


phj_schema = PhjSchema()
phjs_schema = PhjSchema(many=True)
