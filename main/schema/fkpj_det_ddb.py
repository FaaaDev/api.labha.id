from ..shared.shared import ma


class FkpjDetSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'fk_id', 'inv_id', 'sale_id', 'inv_date', 'total', 'total_pay')


fkpjd_schema = FkpjDetSchema()
fkpjds_schema = FkpjDetSchema(many=True)
