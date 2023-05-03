from main.shared.shared import ma

class MaterialSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'um_id', 'prod_id', 'unit_id', 'qty')


material_schema = MaterialSchema()
materials_schema = MaterialSchema(many=True)