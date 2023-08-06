class AbstractUser:
    def __init__(self, **options):
        self._name = options.get('name')
        self._id = options.get('id')
        self._account_id = options.get('account_id')
    
    def __str__(self):
        ret = f"[gd.AbstractUser]\n[Name:{self.name}]\n[ID:{self.id}]\n[AccountID:{self.account_id}]"
        return ret
        
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    @property
    def account_id(self):
        return self._account_id
    
    def to_user(self):
        from .client import client
        user = client().get_user(str(self.account_id))
        return user
