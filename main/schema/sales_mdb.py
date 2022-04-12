from main.shared.shared import ma

class SalesSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'sales_code', 'sales_name', 'sales_ket')


sales_schema = SalesSchema()
saless_schema = SalesSchema(many=True)