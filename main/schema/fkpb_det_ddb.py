from ..shared.shared import ma


class FkpbDetSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "fk_id", "inv_id", "ord_id", "inv_date", "total", "total_pay")


fkpbd_schema = FkpbDetSchema()
fkpbds_schema = FkpbDetSchema(many=True)
