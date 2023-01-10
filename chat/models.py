from django.db import models
from pickle import TRUE
from django.db import models
import os
import uuid
import random
from datetime import datetime 

def user_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.now()
    path = "media/uploads/{}/{}/{}/".format(todays_date.year, todays_date.month, todays_date.day)
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))
    # Filename reformat
    filename_reformat = stringId + randInt + extension
    return os.path.join(path, filename_reformat)

class Category(models.Model):
    Name = models.CharField(max_length=200,null=False,blank=False)
    Active=models.BooleanField(default=True)    
    def __str__(self):
        return self.Name 


class CardNumber(models.Model):
    CardNumber = models.CharField(max_length=200,blank=False, verbose_name = "Card Number")
    Person =models.ForeignKey('Person',on_delete=models.CASCADE, blank=False)
    def __str__(self):
        return self.Person.Name +" "+self.CardNumber

class Person(models.Model):
    Image = models.ImageField(upload_to=user_directory_path,blank=True,null=True)
    Name = models.CharField(max_length=200,blank=False, verbose_name = "Name")
    # Cards =models.ForeignKey(CardNumber,on_delete=models.CASCADE, blank=True)
    MemberNumber = models.CharField(max_length=200,blank=False, verbose_name = "Member Number")
    organisation = models.CharField(max_length=200,blank=False, verbose_name = "Organisation")
    Categorys= models.ManyToManyField(Category, verbose_name = "Category's")
    Details = models.TextField(max_length=500,blank=True,verbose_name = "Details")
    StartDate =models.DateField(null=True,blank=False,verbose_name="Starting time")
    def __str__(self):
        return self.Name +" ("+self.MemberNumber+")"

class GuestEntry(models.Model):
    Name = models.CharField(max_length=200,blank=False, verbose_name = "Name")
    CardNumber=models.CharField(max_length=200,blank=False, null=True, verbose_name = "Card Number")
    Entry= models.ForeignKey('Entry', on_delete=models.CASCADE,null=False,blank=False)
    EntryTime=models.DateTimeField(blank=False,null=True, verbose_name = "Entry Time")
    IdChecked= models.BooleanField()
    ExitTime=models.DateTimeField(blank=True,null=True, verbose_name = "Exit Time")

    def __str__(self):
        return self.Name    

class Entry(models.Model):
    Customer= models.ForeignKey(Person, on_delete=models.CASCADE,null=False,blank=False)
    EntryTime=models.DateTimeField(blank=False, verbose_name = "Entry Time")
    GuestEntrys= models.ManyToManyField(GuestEntry)
    ExitTime=models.DateTimeField(blank=True,null=True, verbose_name = "Exit Time")
                                                                            
    def __str__(self):
        return self.Customer.Name  

CHOICES = (
    ('1','IN'),
    ('2', 'OUT'),
)

class DeviceRegister(models.Model):
    IP = models.CharField(max_length=200,blank=False, verbose_name = "IP")
    Port=models.IntegerField(blank=False,verbose_name = "Port")
    DeviceType = models.CharField(max_length=6, choices=CHOICES, default='1',verbose_name = "DeviceType")
    Timeout=models.IntegerField(blank=False,verbose_name = "Timeout",default=5)
    Password=models.CharField(max_length=200,blank=False, verbose_name = "Password",default='0')
    def __str__(self):
        return self.IP+":"+str(self.Port)






