from main.shared.shared import ma

class GroupProMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'div_code', 'acc_sto', 'acc_send',
    'acc_terima', 'hrg_pokok', 'acc_penj', 'potongan', 'pengembalian', 'selisih')


groupPro_schema = GroupProMdb()
groupPros_schema = GroupProMdb(many=True)