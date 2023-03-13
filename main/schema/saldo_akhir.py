from ..shared.shared import ma

class SldAkhirSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'acc_code', 'date', 'saldo', 'posting', 'user_id')


sld_akhir_schema = SldAkhirSchema()
sld_akhirs_schema = SldAkhirSchema(many=True)