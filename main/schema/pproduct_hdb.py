from main.shared.shared import ma


class PproductSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pp_code", "pp_date", "user_id")


pproduct_schema = PproductSchema()
pproducts_schema = PproductSchema(many=True)
