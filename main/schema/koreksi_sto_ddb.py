from ..shared.shared import ma

class KorStoddbSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'kor_id', 'prod_id', 'unit_id', 'location', 'dbcr', 'qty')


korStoddb_schema = KorStoddbSchema()
korStoddbs_schema = KorStoddbSchema(many=True)