from main.shared.shared import ma

class CurrencyMdb(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'curren_code', 'curren_name', 'curren_date', 'curren_rate')


currency_schema = CurrencyMdb()
currencys_schema = CurrencyMdb(many=True)