from main.shared.shared import ma

class SjasaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'so_id', 'sup_id', 'jasa_id', 'unit_id', 'qty', 'price', 'disc', 'total')


sjasa_schema = SjasaSchema()
sjasas_schema = SjasaSchema(many=True)