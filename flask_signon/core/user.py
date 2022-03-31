class BaseUser:
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_staff(self):
        return False
    
    @property
    def is_superuser(self):
        return False
    
    def get_uid(self):
        raise NotImplementedError("You must implement this method in your class")


class AnonymousUser(BaseUser):
    @property
    def is_authenticated(self):
        return False
    
    @property
    def is_active(self):
        return False
    
    @property
    def is_anonymous(self):
        return True
