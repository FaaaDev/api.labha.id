from main.shared.shared import ma

class FprodSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'orm_id', 'prod_id', 'unit_id', 'qty', 'aloc')


fprod_schema = FprodSchema()
fprods_schema = FprodSchema(many=True)