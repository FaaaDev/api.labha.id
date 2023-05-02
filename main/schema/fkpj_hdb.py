from ..shared.shared import ma


class FkpjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'fk_code', 'fk_date', 'pel_id', 'fk_tax', 'fk_ppn', 'fk_lunas', 'fk_desc')


fkpj_schema = FkpjSchema()
fkpjs_schema = FkpjSchema(many=True)
