from ..shared.shared import ma


class IacqSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "inc_id", "sale_id", "sa_id", "value", "payment", "dp")


iacq_schema = IacqSchema()
iacqs_schema = IacqSchema(many=True)
