from ..shared.shared import ma


class RpbbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "pl_id",
            "prod_id",
            "saldo",
            "plan",
            "sisa",
            "sugestion",
            "loc_id",
            "date_created",
            "date_updated",
        )


rpbb_schema = RpbbSchema()
rpbbs_schema = RpbbSchema(many=True)
