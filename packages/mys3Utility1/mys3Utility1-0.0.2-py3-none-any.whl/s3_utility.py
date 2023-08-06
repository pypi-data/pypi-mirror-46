import boto3

class S3Utility():
    
    def __init__(self):
        self.client = None
        print("entering constructor")
        
        
    def configure(self,access_key,secret_key):
        self.client = boto3.client(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key, 
            service_name = "s3"
        )
        
    def get_buckets(self):
        reponse = self.client.list_bucket()
        print(reponse)
        return reponse
    
    