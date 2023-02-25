from main.shared.shared import ma


class DprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "ord_id",
            "po_id",
            "pprod_id",
            "prod_id",
            "unit_id",
            "order",
            "price",
            "disc",
            "location",
            "laporan",
            "nett_price",
            "total_fc",
            "total",
        )


dprod_schema = DprodSchema()
dprods_schema = DprodSchema(many=True)
