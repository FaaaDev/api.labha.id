from main.shared.shared import ma

class KorStoSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'code', 'date', 'dep_id', 'proj_id', 'user_id')


korSto_schema = KorStoSchema()
korStos_schema = KorStoSchema(many=True)