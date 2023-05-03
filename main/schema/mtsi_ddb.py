from ..shared.shared import ma


class MtsiddbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'mtsi_id', 'prod_id', 'unit_id', 'qty', 'qty_terima')


mtsiddb_schema = MtsiddbSchema()
mtsiddbs_schema = MtsiddbSchema(many=True)
