from ..shared.shared import ma


class KoreksiPiuSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "code",
            "date",
            "cus_id",
            "type_kor",
            "acc_lwn",
            "value",
            "due_date",
            "desc",
            "user_id",
        )


korPiut_schema = KoreksiPiuSchema()
korPiuts_schema = KoreksiPiuSchema(many=True)
