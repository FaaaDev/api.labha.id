from main.shared.shared import ma


class UphSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pbb_id", "acc_id")


uph_schema = UphSchema()
uphs_schema = UphSchema(many=True)
