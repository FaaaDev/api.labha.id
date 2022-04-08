from main.shared.shared import ma

class CcostSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'keterangan')


ccost_schema = CcostSchema()
ccosts_schema = CcostSchema(many=True)