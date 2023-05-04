from main.shared.shared import ma

class MatBiayaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'um_id', 'acc_id', 'value', "desc")


mat_biaya_schema = MatBiayaSchema()
mat_biayas_schema = MatBiayaSchema(many=True)