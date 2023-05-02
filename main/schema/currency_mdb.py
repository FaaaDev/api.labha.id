from ..shared.shared import ma

class CurrencyMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'date', 'rate')


currency_schema = CurrencyMdb()
currencys_schema = CurrencyMdb(many=True)