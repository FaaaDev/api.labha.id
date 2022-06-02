from main.shared.shared import ma


class DordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id',
                  'ord_code',
                  'ord_date',
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
                  'status',
                  'print')


dord_schema = DordSchema()
dords_schema = DordSchema(many=True)
