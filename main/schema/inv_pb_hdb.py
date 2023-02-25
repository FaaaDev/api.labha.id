from main.shared.shared import ma


class InvpbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'inv_code', 'inv_date', 'ord_id', 'inv_tax', 'inv_ppn', 'inv_lunas', 'inv_desc', 'total_bayar', 'faktur')


invpb_schema = InvpbSchema()
invpbs_schema = InvpbSchema(many=True)
