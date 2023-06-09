from ..shared.shared import ma


class BankMdb(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "BANK_CODE",
            "BANK_NAME",
            "BANK_DESC",
            "CURRENCY",
            "acc_id",
            "user_entry",
            "user_edit",
            "entry_date",
            "edit_date",
            "comp_id",
        )


bank_schema = BankMdb()
banks_schema = BankMdb(many=True)
