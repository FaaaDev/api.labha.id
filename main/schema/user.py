from main.shared.shared import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('uid', 'username', 'email', 'phone', 'image', 'dob')


user_schema = UserSchema()
users_schema = UserSchema(many=True)