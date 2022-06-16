from main.shared.shared import ma


class OrdpjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id',
                  'ord_code',
                  'ord_date',
                  'so_id',
                  'invoice',
                  'pel_id',
                  'ppn_type',
                  'sub_addr',
                  'sub_id',
                  'slsm_id',
                  'req_date',
                  'top',
                  'due_date',
                  'split_inv',
                  'prod_disc',
                  'jasa_disc',
                  'total_disc',
                  'status',
                  'print')


ordpj_schema = OrdpjSchema()
ordpjs_schema = OrdpjSchema(many=True)
