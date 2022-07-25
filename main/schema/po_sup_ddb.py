from main.shared.shared import ma


class PoSupSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'po_id', 'sup_id', 'prod_id', 'price', 'image')


poSup_schema = PoSupSchema()
poSups_schema = PoSupSchema(many=True)