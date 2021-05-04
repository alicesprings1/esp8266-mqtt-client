# def config(client_id,pub_topic,user='admin',password='admin',server='120.77.223.118',port=1883):
#     client_id=client_id
#     pub_topic=pub_topic
#     user=user
#     password=password
#     server=server
#     port=port

class Config:
    def __init__(self,client_id,pub_topic,user='admin',password='admin',server='120.77.223.118',port=1883):
        self.client_id=client_id
        self.pub_topic=pub_topic
        self.user=user
        self.password=password
        self.server=server
        self.port=port