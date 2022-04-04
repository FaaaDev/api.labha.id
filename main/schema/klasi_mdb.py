from main.shared.shared import ma

class KlasiMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'klasiname')


klasi_schema = KlasiMdb()
klasies_schema = KlasiMdb(many=True)