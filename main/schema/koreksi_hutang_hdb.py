from main.shared.shared import ma


class KoreksiHutSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "code",
            "date",
            "sup_id",
            "tipe",
            "value",
            "acc_lwn",
            "due_date",
            "desc",
            "user_id",
        )


korHut_schema = KoreksiHutSchema()
korHuts_schema = KoreksiHutSchema(many=True)
