from main.shared.shared import ma

class SprodSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'so_id', 'prod_id', 'unit_id', 'location', 'request','price','order', 'remain', 'disc', 'nett_price', 'total')


sprod_schema = SprodSchema()
sprods_schema = SprodSchema(many=True)