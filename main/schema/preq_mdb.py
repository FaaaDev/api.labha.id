from main.shared.shared import ma

class PreqSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'req_code', 'req_date', 'req_dep', 'req_ket', 'refrence', 'ref_sup', 'ref_ket', 'status')


preq_schema = PreqSchema()
preqs_schema = PreqSchema(many=True)