from ..shared.shared import ma


class KategMdb(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'name', 'kode_klasi', 'kode_saldo',
                  'imp', 'user_id', 'comp_id')


kateg_schema = KategMdb()
kategs_schema = KategMdb(many=True)
