from main.shared.shared import ma

class RjasaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'preq_id', 'sup_id', 'jasa_id', 'unit_id', 'qty', 'price', 'disc', 'total')


rjasa_schema = RjasaSchema()
rjasas_schema = RjasaSchema(many=True)