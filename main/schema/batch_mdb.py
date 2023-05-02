from ..shared.shared import ma


class BatchSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "bcode", "batch_date", "plan_id", "dep_id")


batch_schema = BatchSchema()
batchs_schema = BatchSchema(many=True)
