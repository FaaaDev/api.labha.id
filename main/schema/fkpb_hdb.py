from main.shared.shared import ma


class FkpbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'fk_code', 'fk_date', 'ord_id', 'fk_tax', 'fk_ppn', 'fk_lunas')


fkpb_schema = FkpbSchema()
fkpbs_schema = FkpbSchema(many=True)
