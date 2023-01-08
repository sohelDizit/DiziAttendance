from zk import ZK, const
import time
import requests

def LiveCapture():
    conn = None
    zk = ZK('172.20.0.71', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        conn = zk.connect()
        print("Connected")
        for attendance in conn.live_capture():
            if attendance is None:
                # print("attendance is None")
                pass
            else:
                x = requests.get('http://127.0.0.1:8099/lobby1/'+str(attendance.uid)+'/')
                print ('+ UID #{}'.format(attendance.uid))

    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        print ("Disconnected")
        if conn:
            conn.disconnect()
    


LiveCapture()
   