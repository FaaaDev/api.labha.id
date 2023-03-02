from main.shared.shared import ma


class ExpSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "exp_code",
            "exp_date",
            "type_trx",
            "acq_sup",
            "acq_pay",
            "acq_kas",
            "bank_ref",
            "bank_acc",
            "giro_num",
            "giro_date",
            "bank_id",
            "exp_type",
            "kas_acc",
            "exp_bnk",
            "type_acc",
            "exp_dep",
            "exp_prj",
            "dp_type",
            "dp_sup",
            "dp_kas",
            "dp_bnk",
            "approve",
            "user_id",
        )


exp_schema = ExpSchema()
exps_schema = ExpSchema(many=True)
