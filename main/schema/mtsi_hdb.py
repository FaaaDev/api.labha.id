from ..shared.shared import ma


class MtsiSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "mtsi_code",
            "mtsi_date",
            "loc_from",
            "loc_to",
            "dep_id",
            "prj_id",
            "doc",
            "doc_date",
            "desc",
            "approve",
        )


mtsi_schema = MtsiSchema()
mtsis_schema = MtsiSchema(many=True)
