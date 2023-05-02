from ..shared.shared import ma


class OvhSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pbb_id", "acc_id")


ovh_schema = OvhSchema()
ovhs_schema = OvhSchema(many=True)
