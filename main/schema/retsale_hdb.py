from ..shared.shared import ma


class RetSaleSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ret_code', 'ret_date', 'sale_id')


retsale_schema = RetSaleSchema()
retsales_schema = RetSaleSchema(many=True)
