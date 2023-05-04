from main.shared.shared import ma


class UsageMatSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "code",
            "date",
            "dep_id",
            "loc_id",
            "post",
            "closing",
            "user_id",
        )


usage_mat_schema = UsageMatSchema()
usage_mats_schema = UsageMatSchema(many=True)
