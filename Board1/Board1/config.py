class Config:
    
    def __init__(self,client_id,**kw):
        self.user='username'
        self.password='password'
        self.server='mqtt_server_ip'
        self.port=1883
        self.client=None
        self.client_id=client_id  
   
