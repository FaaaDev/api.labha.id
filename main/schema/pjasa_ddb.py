from main.shared.shared import ma

class PjasaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'po_id', 'preq_id', 'sup_id', 'jasa_id', 'unit_id', 'order', 'price', 'disc', 'total')


pjasa_schema = PjasaSchema()
pjasas_schema = PjasaSchema(many=True)