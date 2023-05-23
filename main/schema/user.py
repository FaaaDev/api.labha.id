from ..shared.shared import ma

class UserSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'username', 'name', 'email', 'confirmation_code', 'remember_token', 'active', 'confirmed', 'created_at', 'updated_at', 'company')


user_schema = UserSchema()
users_schema = UserSchema(many=True)