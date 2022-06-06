from main.shared.shared import ma


class ReprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ret_id', 'prod_id', 'unit_id', 'retur', 'price', 'disc', 'nett_price', 'total')


reprod_schema = ReprodSchema()
reprods_schema = ReprodSchema(many=True)
