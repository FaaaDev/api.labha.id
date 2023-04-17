from ..shared.shared import ma


class PnlSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "cp_id", "klasi", "user_id")


pnl_schema = PnlSchema()
pnls_schema = PnlSchema(many=True)
