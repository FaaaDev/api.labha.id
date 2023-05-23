from main.shared.shared import ma


class DirectBatchSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "bcode",
            "batch_date",
            "forml_id",
            "mat_id",
            "dep_id",
            "loc_id",
            "msn_id",
            "total",
            "pb",
            "post",
            "closing",
            "prdc_rm",
            "user_id",
        )


dbatch_schema = DirectBatchSchema()
dbatchs_schema = DirectBatchSchema(many=True)
