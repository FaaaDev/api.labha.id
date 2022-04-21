from main.shared.shared import ma

class CompSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'cp_name', 'cp_addr', 'cp_ship_addr', 'cp_telp', 'cp_email', 'cp_webs', 'cp_npwp', 'cp_coper', 'cp_logo', 'multi_currency', 'appr_po', 'appr_payment', 'over_stock', 'discount', 'tiered', 'rp', 'over_po')


comp_shcema = CompSchema()
comps_schema = CompSchema(many=True)