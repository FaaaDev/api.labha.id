from ..shared.shared import ma


class DincSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "inc_id",
            "acc_code",
            "acc_bnk",
            "bnk_code",
            "value",
            "fc",
            "desc",
        )


dinc_schema = DincSchema()
dincs_schema = DincSchema(many=True)
