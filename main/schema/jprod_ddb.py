from main.shared.shared import ma


class JprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "pj_id",
            "sprod_id",
            "preq_id",
            "rprod_id",
            "prod_id",
            "location",
            "unit_id",
            "order",
            "price",
            "disc",
            "nett_price",
            "total_fc",
            "total",
        )


jprod_schema = JprodSchema()
jprods_schema = JprodSchema(many=True)
