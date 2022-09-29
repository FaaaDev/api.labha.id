from main.shared.shared import ma


class IacqSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'inc_id', 'sale_id', 'value', 'payment')


iacq_schema = IacqSchema()
iacqs_schema = IacqSchema(many=True)
