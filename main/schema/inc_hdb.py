from main.shared.shared import ma


class IncSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "inc_code",
            "inc_date",
            "inc_type",
            "inc_acc",
            "inc_prj",
            "acq_cus",
            "acq_pay",
            "giro_bnk",
            "bank_id",
            "bank_ref",
            "giro_num",
            "giro_date",
            "dp_type",
            "dp_cus",
            "dp_kas",
            "dp_bnk",
            "approve",
            "user_id",
        )


inc_schema = IncSchema()
incs_schema = IncSchema(many=True)
