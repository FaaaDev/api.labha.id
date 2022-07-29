from main.shared.shared import ma


class FprdcSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "fcode",
            "fname",
            "version",
            "rev",
            "desc",
            "active",
            "date_created",
            "date_updated",
        )


fprdc_schema = FprdcSchema()
fprdcs_schema = FprdcSchema(many=True)
