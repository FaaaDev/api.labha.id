from ..shared.shared import ma


class AccddbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "acc_year",
            "acc_month",
            "acc_code",
            "acc_awal",
            "acc_debit",
            "acc_kredit",
            "acc_akhir",
            "sa",
            "from_closing",
            "transfer",
            "user_id",
        )


accddb_schema = AccddbSchema()
accddbs_schema = AccddbSchema(many=True)
