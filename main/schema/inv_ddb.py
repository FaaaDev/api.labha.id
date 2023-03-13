from main.shared.shared import ma


class InvddbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "inv_year",
            "inv_month",
            "inv_code",
            "loc_code",
            "inv_awal",
            "inv_debit",
            "inv_kredit",
            "inv_akhir",
            "qty_awal",
            "qty_debit",
            "qty_kredit",
            "qty_akhir",
            "hpp",
            "sa",
            "from_closing",
            "user_id",
        )


invddb_schema = InvddbSchema()
invddbs_schema = InvddbSchema(many=True)
