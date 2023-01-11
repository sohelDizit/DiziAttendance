from django.apps import AppConfig,apps
import threading
from zk import ZK, const
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
from django.utils import timezone
import os


def LiveCaptureIn(ip,port,timeout,password):
    from .models import Person,CardNumber
    conn = None
    zk = ZK(ip, port=port, timeout=timeout, password=password, force_udp=False, ommit_ping=False)
    try:
        conn = zk.connect()
        layer = get_channel_layer()
        print("LiveCaptureIn Connected")
        for attendance in conn.live_capture():
            if attendance is not None:     
                print("-------------------Entered-----------------------")          
                card_obj=CardNumber.objects.filter(CardNumber=attendance.user_id)[:1]          
                if card_obj:
                    person=card_obj[0].Person
                    async_to_sync(layer.group_send)('test', {"type": "chat_message", "Redirect": "/member/"+str(person.id)})              
                    print ('+LiveCaptureIn UID  #{}'.format(attendance.user_id))
                else:
                    async_to_sync(layer.group_send)('test', {"type": "chat_message",'UID':attendance.user_id})              

    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        print ("Disconnected")
        if conn:
            conn.disconnect()
    

def LiveCaptureOut(ip,port,timeout,password):
    from .models import Person,GuestEntry,Entry,CardNumber
    conn = None
    zk = ZK(ip, port=port, timeout=timeout, password=password, force_udp=False, ommit_ping=False)
    try:
        conn = zk.connect()
        print("LiveCaptureOut Connected and IP:"+ip)
        layer = get_channel_layer()
        for attendance in conn.live_capture():
            try:
                if attendance != None:
                    print ('+ UID #{}'.format(attendance.user_id))
                    card_obj=CardNumber.objects.filter(CardNumber=attendance.user_id)[:1]    
                    print("----------------------------------------------------------------") 
                    if card_obj:     
                        personEntry=Entry.objects.filter(Customer=card_obj[0].Person,ExitTime=None).order_by('-EntryTime')
                        if personEntry:
                            personEntry= personEntry[0]
                            active_guest= personEntry.GuestEntrys.filter(ExitTime=None)
                            if active_guest:
                                async_to_sync(layer.group_send)('test', {"type": "chat_message", "message": ("You have %s Guest"%(len(active_guest)))})   
                                continue; 

                            personEntry.ExitTime =datetime.now()    
                            personEntry.save()  
                            async_to_sync(layer.group_send)('test', {"type": "chat_message","OtherMessage":personEntry.Customer.Name+" has Existed" ,"Redirect": "/thanks/"+str(personEntry.id)})    
                    else:
                        guests= GuestEntry.objects.filter(CardNumber=attendance.user_id,ExitTime=None)
                        if guests:
                            for guest in guests:
                                guest.ExitTime=datetime.now(tz=timezone.utc)
                                guest.save()
                                entry= Entry.objects.filter(GuestEntrys__CardNumber=attendance.user_id).order_by('-id')[:1]
                                if entry:
                                    async_to_sync(layer.group_send)('test', {"type": "chat_message", "OtherMessage":guest.Name+" has Exited" ,  "Redirect": "/member/"+str(entry[0].Customer.id)})
                        else:
                            async_to_sync(layer.group_send)('test', {"type": "chat_message", "OtherMessage":"Card not Found" })
                            
            
            except Exception as e:
                print ("Process terminate : {}".format(e))

    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        print ("Disconnected")
        if conn:
            conn.disconnect()
    

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
        if os.environ.get('RUN_MAIN')==None:
            return
        print("On startup")
        from .models import DeviceRegister
        for device in  DeviceRegister.objects.all():
            if device.DeviceType=='1':
                print(device.IP)
                # threading.Thread(target=LiveCaptureIn(device.IP,device.Port,device.Timeout,device.Password)).start()
                threading.Thread(target=LiveCaptureIn,args =(device.IP,device.Port,device.Timeout,device.Password)).start()
            elif device.DeviceType=='2':
                print(device.IP)
                threading.Thread(target=LiveCaptureOut,args =(device.IP,device.Port,device.Timeout,device.Password)).start()
        pass
        