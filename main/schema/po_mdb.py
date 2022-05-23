from main.shared.shared import ma

class PoSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'po_code', 'po_date', 'preq_id', 'sup_id', 'ppn_type', 'top', 'due_date', 'split_inv', 'prod_disc', 'jasa_disc', 'total_disc')


po_schema = PoSchema()
pos_schema = PoSchema(many=True)