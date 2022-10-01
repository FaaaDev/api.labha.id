from main.shared.shared import ma


class PprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'po_id', 'preq_id', 'rprod_id', 'prod_id', 'unit_id', 'order', 'remain', 'price', 'disc', 'nett_price', 'total')


pprod_schema = PprodSchema()
pprods_schema = PprodSchema(many=True)
