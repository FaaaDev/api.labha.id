class UserModel:
    id = None
    username = None
    name = None
    email = None
    active = None
    confirmation_code = None
    remember_token = None
    confirmed = None
    created_at = None
    updated_at = None
    company = None
    
    def __init__(self, data):
        self.id = data["id"]
        self.username = data['username']
        self.name = data['name']
        self.email = data['email']
        self.confirmation_code = data['confirmation_code']
        self.remember_token = data['remember_token']

        
