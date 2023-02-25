from main.shared.shared import ma


class DordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id',
                  'ord_code',
                  'ord_date',
                  'no_doc',
                  'doc_date',
                  'invoice',
                  'faktur',
                  'po_id',
                  'dep_id',
                  'sup_id',
                  'top',
                  'due_date',
                  'split_inv',
                  'prod_disc',
                  'jasa_disc',
                  'total_disc',
                  'total_b',
                  'total_bayar',
                  'same_sup',
                  'status',
                  'print')


dord_schema = DordSchema()
dords_schema = DordSchema(many=True)
