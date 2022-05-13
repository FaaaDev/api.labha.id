from main.shared.shared import ma

class PajakSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'name', 'nilai')


pajk_schema = PajakSchema()
pajks_schema = PajakSchema(many=True)