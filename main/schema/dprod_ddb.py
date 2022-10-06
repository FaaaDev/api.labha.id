from main.shared.shared import ma


class DprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ord_id', 'faktur', 'po_id', 'pprod_id', 'prod_id', 'unit_id', 'order', 'price', 'disc', 'location', 'laporan', 'nett_price', 'total')


dprod_schema = DprodSchema()
dprods_schema = DprodSchema(many=True)
