from main.shared.shared import ma


class ExpSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'exp_code', 'exp_date', 'exp_type', 'exp_acc', 'exp_prj', 'acq_sup', 'acq_pay', 'kas_acc', 'bank_id', 'bank_ref', 'giro_num', 'giro_date', 'approve')


exp_schema = ExpSchema()
exps_schema = ExpSchema(many=True)
