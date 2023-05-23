from main.shared.shared import ma


class ProdSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "code",
            "name",
            "group",
            "type",
            "codeb",
            "unit",
            "weight",
            "dm_panjang",
            "dm_lebar",
            "dm_tinggi",
            "suplier",
            "b_price",
            "s_price",
            "barcode",
            "metode",
            "max_stock",
            "min_stock",
            "re_stock",
            "lt_stock",
            "max_order",
            "image",
            "ns",
            "ket",
            "imp",
        )


prod_schema = ProdSchema()
prods_schema = ProdSchema(many=True)
