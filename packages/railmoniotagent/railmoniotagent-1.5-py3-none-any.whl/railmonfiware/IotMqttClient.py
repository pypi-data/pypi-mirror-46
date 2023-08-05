import paho.mqtt.client as mqtt
import time
import base64
import http.client
import json


class Mqttclient:
    #init
   
    def __init__(self,ipadress,port,cbrokeradress,cbrokerport,connection_name):
        self.ipadress=ipadress
        self.port=port
        self.cbrokeradress=cbrokeradress
        self.cbrokerport=cbrokerport
        self.message="nothing"
        self.subClient=mqtt.Client(connection_name)
    def set_Entity(self,ipadress,entity_name,entity_type):
        self.entity_name=entity_name
        self.entity_type=entity_type
    def set_Service(self,servicename,servicepath):
        self.servicename=servicename
        self.servicepath=servicepath




        
    




    #create a service for iotagent
    def create_Service(self,apikey,thingtype,resource,servicename,servicepath):
       self.apikey=apikey
       self.thingtype=thingtype
       self.resource=resource
       self.servicename=servicename
       self.servicepath=servicepath

       conn = http.client.HTTPConnection(""+self.ipadress+":"+self.port)

       payload = "{ \"services\": [ { \"apikey\": \""+apikey+"\", \"cbroker\": \""+self.cbrokeradress+":"+self.cbrokerport+"\", \"entity_type\": \""+thingtype+"\", \"resource\": \""+resource+"\" } ] }"

       headers = {
       'content-type': "application/json",
       'fiware-service': ""+self.servicename,
       'fiware-servicepath': ""+self.servicepath
       }

       conn.request("POST", "/iot/services", payload, headers)

       res = conn.getresponse()
       data = res.read()

       print(data.decode("utf-8"))
       print("Service created.")


    #send a command to execute to the iot device
    def iota_Send_Command(self,cmd,value):
        import http.client

        conn = http.client.HTTPConnection(""+self.ipadress+":"+self.port)
        payload = "{ \"contextElements\": [ { \"type\": \"MyRaspi\", \"isPattern\": \"false\", \"id\": \"tiga:myraspi\", \"attributes\": [ { \"name\": \""+cmd+"\", \"type\": \"command\", \"value\": \""+value+"\" } ], \"static_attributes\": [ {\"name\":\"refStore\", \"type\": \"Relationship\",\"value\": \"tiga:raspi\"} ] } ], \"updateAction\": \"UPDATE\" }"

        headers = {
        'content-type': "application/json",
        'fiware-service': "openiot",
        'fiware-servicepath': "/"
        }

        conn.request("POST", "/v1/updateContext", payload, headers)

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    #
    def pub_Command (self,cmd):

     conn = http.client.HTTPConnection(""+self.cbrokeradress+":"+self.cbrokerport)

     payload = "{ \""+cmd+"\": { \"type\" : \"command\", \"value\" : \"pls\" } }"

     headers = {
    'content-type': "application/json",
    'fiware-service': ""+self.servicename,
    'fiware-servicepath': ""+self.servicepath
     }

     conn.request("PATCH", "/v2/entities/"+self.entity_name+"/attrs", payload, headers)

     res = conn.getresponse()
     data = res.read()
     print(data.decode("utf-8"))
     print("command:",cmd," was sent to the device:",self.deviceid)



    def pub_Message(self,devid,topic,command,message):
        self.subClient.connect(self.ipadress,31705)
        self.subClient.publish("/"+topic+"/"+devid+"/cmd",""+devid+"@"+command+"|"+message)

 


    #

#client=Mqttclient("192.168.1.242","32383")
#client.iota_Send_Command("lamp","LAMP ON")

    #create a device
    def create_Device(self,deviceid,entityname,entitytype,commands):
      conn = http.client.HTTPConnection(""+self.ipadress+":"+self.port)
      self.deviceid=deviceid
      self.entity_name=entityname
      self.entitytype=entitytype
      self.commands=commands


      payload = "{ \"devices\": [ { \"device_id\": \""+self.deviceid+"\", \"entity_name\": \""+self.entity_name+"\", \"entity_type\": \""+self.entitytype+"\", \"protocol\": \"PDI-IoTA-UltraLight\", \"transport\": \"MQTT\", \"commands\": [ { \"name\": \""+commands[0]+"\", \"type\": \"command\" }, {\"name\":\""+commands[1]+"\",\"type\":\"command\"} ] } ] }"
      headers = {
      'content-type': "application/json",
      'fiware-service': ""+self.servicename,
      'fiware-servicepath': ""+self.servicepath
      }

      conn.request("POST", "/iot/devices", payload, headers)

      res = conn.getresponse()
      data = res.read()
      print(data.decode("utf-8"))
      print("Process complete please subscribe the device to the topic\n")
      print("/"+self.apikey+"/"+""+self.deviceid+"/"+"cmd")

    
    

    #publish measure

    #subscribe cmd


    #mqtt connect


    #get command result
    def result_cmd(self):

     conn = http.client.HTTPConnection(""+self.cbrokeradress+":"+self.cbrokerport)

     payload = "type="+self.entitytype

     headers = {
     'fiware-service': ""+self.servicename,
     'fiware-servicepath': ""+self.servicepath
     }

     conn.request("GET", "/v2/entities/"+self.entity_name, payload, headers)

     res = conn.getresponse()
     data = res.read()

     print(data.decode("utf-8"))


     #client sub
    def sub_Server(self,name,topic):
         self.clientname=name
         
         #self.subClient.on_message=self.on_message
         self.subClient.connect(self.ipadress,31705)
         self.subClient.subscribe(topic)
         print("subcribing the topic "+topic)
         self.subClient.loop_forever()

    def get_Device_Status(self,entity_name,entity_type,service_name,service_path):
        conn = http.client.HTTPConnection("192.168.1.242:32562")

        headers = {
        'accept': "application/json",
        'fiware-service': ""+service_name,
        'fiware-servicepath': ""+service_path
        }

        conn.request("GET", "/v2/entities/"+entity_name+"?type="+entity_type, headers=headers)
        res = conn.getresponse()
        data = res.read()
        x=json.loads(data.decode('utf-8'))
        print(json.loads(data.decode('utf-8')))
        print(x["cam_info"])
     


         


    
     
#to publish this package
#python setup.py sdist bdist_wheel

#publish to testpypi
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#publish to pypi
# twine upload dist/*

#show logs
#kubectl logs -f mosquitto-6bcbd8974c-f526j | grep "1042019"
    

