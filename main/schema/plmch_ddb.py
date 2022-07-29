from main.shared.shared import ma


class PlmchSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", 'pl_id', 'mch_id')


plmch_schema = PlmchSchema()
plmchs_schema = PlmchSchema(many=True)
