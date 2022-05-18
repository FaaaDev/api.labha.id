from main.shared.shared import ma

class PajakSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'type', 'name', 'nilai', 'cutting', 'acc_sls_fax', 'acc_pur_fax', 'combined')


pajk_schema = PajakSchema()
pajks_schema = PajakSchema(many=True)