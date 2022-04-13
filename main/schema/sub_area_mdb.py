from main.shared.shared import ma

class SubAreaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'sub_code', 'sub_area_code', 'sub_name', 'sub_ket')


sub_area_schema = SubAreaSchema()
sub_areas_schema = SubAreaSchema(many=True)