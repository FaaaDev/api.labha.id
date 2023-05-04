from main.shared.shared import ma

class BtcrejcSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'btc_id', 'prod_id', 'unit_id', 'loc_id', 'qty', 'aloc')


breject_schema = BtcrejcSchema()
brejects_schema = BtcrejcSchema(many=True)