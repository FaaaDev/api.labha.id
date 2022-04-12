from main.shared.shared import ma

class SubAreaSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'sub_code', 'sub_areaCode' 'sub_name', 'sub_ket')


subArea_schema = SubAreaSchema()
subAreas_schema = SubAreaSchema(many=True)