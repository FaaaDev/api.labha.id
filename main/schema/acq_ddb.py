from ..shared.shared import ma

class AcqSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'exp_id', 'fk_id', 'value', 'payment', 'dp')


acq_schema = AcqSchema()
acqs_schema = AcqSchema(many=True)