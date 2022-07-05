from main.shared.shared import ma


class StCardSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "trx_code",
            "trx_date",
            "trx_dbcr",
            "trx_type",
            "trx_seku",
            "trx_qty",
            "trx_amnt",
            "trx_total",
            "trx_hpok",
            "trx_sprice",
            "trx_disc",
            "prod_id",
            "loc_id",
            "scu_code",
            "flag",
            "kode_kasir",
        )


st_card_schema = StCardSchema()
st_cards_schema = StCardSchema(many=True)
