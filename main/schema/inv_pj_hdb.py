from main.shared.shared import ma


class InvoicePjSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'inv_code', 'inv_date', 'sale_id', 'inv_tax', 'inv_ppn', 'inv_lunas', 'inv_desc', 'total_bayar', 'faktur')


invpj_schema = InvoicePjSchema()
invpjs_schema = InvoicePjSchema(many=True)
