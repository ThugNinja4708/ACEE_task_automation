import logging
logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', datefmt="%d-%b-%y %H:%M:%S")
class Bad_Response(Exception):
    def __init__(self,message=None,response=None):
        self.message = message
        self.response = response["svcMessage"]
        print ("m",response["svcMessage"])
        print ("r",response)
        super().__init__(self.message)
        logging.error(self.message)
        

