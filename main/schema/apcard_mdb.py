from ..shared.shared import ma


class APCardSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "trx_code",
            "sup_id",
            "ord_id",
            "ord_date",
            "ord_due",
            "po_id",
            "acq_id",
            "acq_date",
            "cur_conv",
            "trx_dbcr",
            "trx_type",
            "pay_type",
            "trx_amnh",
            "trx_amnv",
            "acq_amnh",
            "acq_amnv",
            "giro_id",
            "giro_date",
            "sa_id",
            "sa",
            "lunas",
        )


apcard_schema = APCardSchema()
apcards_schema = APCardSchema(many=True)
