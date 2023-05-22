from main.shared.shared import ma

class CurrencyMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'date', 'rate', 'comp_id')


currency_schema = CurrencyMdb()
currencys_schema = CurrencyMdb(many=True)