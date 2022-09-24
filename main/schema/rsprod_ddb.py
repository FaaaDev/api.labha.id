from main.shared.shared import ma


class RsprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'ret_id', 'prod_id', 'unit_id', 'retur', 'price', 'disc', 'nett_price', 'totl', 'location')


rsprod_schema = RsprodSchema()
rsprods_schema = RsprodSchema(many=True)
