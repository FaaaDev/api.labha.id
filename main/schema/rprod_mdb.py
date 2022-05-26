from main.shared.shared import ma


class RprodSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'preq_id', 'prod_id', 'unit_id', 'request', 'remain')


rprod_schema = RprodSchema()
rprods_schema = RprodSchema(many=True)
