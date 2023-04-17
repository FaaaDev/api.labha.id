from ..shared.shared import ma


class TransBankSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "trx_code",
            "trx_date",
            "bank_id",
            "trx_amnt",
            "trx_dbcr",
            "trx_desc",
            "user_id",
        )


trans_bank_schema = TransBankSchema()
trans_banks_schema = TransBankSchema(many=True)
