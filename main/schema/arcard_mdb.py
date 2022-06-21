from main.shared.shared import ma

class ARCardSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'cus_id', 'trx_code', 'trx_date', 'trx_due', 'acq_id', 'acq_date', 'bkt_id',
                 'bkt_date', 'cur_conv',  'trx_dbcr', 'trx_type', 'pay_type', 'trx_amnh', 'trx_amnv',
                 'acq_amnh', 'acq_amnv', 'bkt_amnv', 'bkt_amnh', 'trx_desc', 'giro_id', 'giro_date',
                 'pos_flag', 'loc_id', 'trx_pymnt')


arcard_schema = ARCardSchema()
arcards_schema = ARCardSchema(many=True)