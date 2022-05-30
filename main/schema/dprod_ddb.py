from main.shared.shared import ma


class DprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'do_id', 'prod_id', 'unit_id', 'order', 'price', 'disc', 'nett_price', 'total')


dprod_schema = DprodSchema()
dprods_schema = DprodSchema(many=True)
