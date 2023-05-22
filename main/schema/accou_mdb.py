from main.shared.shared import ma


class AccouSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id', 'acc_code', 'acc_name', 'umm_code', 'kat_code',
                  'dou_type', 'sld_type', 'connect', 'sld_awal', 'level', 'user_id', 'comp_id')


accou_schema = AccouSchema()
accous_schema = AccouSchema(many=True)
