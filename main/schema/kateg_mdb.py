from ..shared.shared import ma

class KategMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'kode_klasi', 'kode_saldo', 'user_id')


kateg_schema = KategMdb()
kategs_schema = KategMdb(many=True)