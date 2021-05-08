class Config:
        
    def __init__(self,**kw):
        self.user='admin'
        self.password='admin'
        self.server='120.77.223.118'
        self.port=1883
        self.client=None
        if 'pin' in kw:
            self.pin=kw['pin']
    
   