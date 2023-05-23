from ..shared.shared import ma


class DjasaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "ord_id",
            "sup_id",
            "jasa_id",
            "unit_id",
            "order",
            "price",
            "disc",
            "total_fc",
            "total",
        )


djasa_schema = DjasaSchema()
djasas_schema = DjasaSchema(many=True)
