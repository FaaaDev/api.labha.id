from ..shared.shared import ma

class AreaPenjualanSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'area_pen_code', 'area_pen_name', 'area_pen_ket')


area_penjualan_schema = AreaPenjualanSchema()
area_penjualans_schema = AreaPenjualanSchema(many=True)