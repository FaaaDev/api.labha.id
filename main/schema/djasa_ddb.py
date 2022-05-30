from main.shared.shared import ma

class DjasaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'do_id', 'sup_id', 'jasa_id', 'unit_id', 'order', 'price', 'disc', 'total')


djasa_schema = DjasaSchema()
djasas_schema = DjasaSchema(many=True)