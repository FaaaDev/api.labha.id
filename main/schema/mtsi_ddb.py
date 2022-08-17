from main.shared.shared import ma

class MtsiddbSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'mtsi_id', 'prod_id', 'unit', 'qty')


mtsiddb_schema = MtsiddbSchema()
mtsiddbs_schema = MtsiddbSchema(many=True)