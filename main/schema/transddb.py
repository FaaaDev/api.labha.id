from main.shared.shared import ma

class TransDDB(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'trx_code', 'trx_date', 'acc_id', 'ccost_id', 'proj_id', 'acq_date', 'cur_id', 'cur_rate', 'trx_vala', 'trx_amnt',
                 'trx_dbcr', 'trx_desc', 'gen_post', 'post_date')


trans_schema = TransDDB()
transs_schema = TransDDB(many=True)