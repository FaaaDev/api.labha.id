from main.shared.shared import ma

class JasaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'desc', 'acc_id')


jasa_schema = JasaSchema()
jasas_schema = JasaSchema(many=True)