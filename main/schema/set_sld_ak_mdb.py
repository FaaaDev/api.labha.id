from ..shared.shared import ma


class SetupSaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "cp_id",
            "sto",
            "pur",
            "pur_shipping",
            "pur_retur",
            "pur_discount",
            "hpp",
            "user_id"
        )


setupsa_shcema = SetupSaSchema()
setupsas_schema = SetupSaSchema(many=True)
