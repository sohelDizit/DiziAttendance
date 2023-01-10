from django.shortcuts import render,HttpResponse
from zk import ZK, const
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time
from .models import Person,Entry,GuestEntry,CardNumber
from datetime import datetime
from django.shortcuts import redirect
import threading
from django.conf import settings

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



def lobby(request):
    return render(request, 'chat/lobby.html')
    
def lobby1(request,pk):
    person = Person.objects.filter(CardNumber=pk)
    if person:
        layer = get_channel_layer()
        async_to_sync(layer.group_send)('test', {"type": "chat_message", "message": "/member/"+str(pk)})
    else:
        pass
    return HttpResponse("done")
    
def ThanksPage(request,pk):
    entry= Entry.objects.get(pk=pk)
    return render(request, "chat/thanks.html",{'entry':entry})



@login_required(login_url='login/')
def Home(request):
    return render(request, "home/index.html")

class Dashboard(LoginRequiredMixin,View):
    template_name = 'home/index.html'
    login_url ='/login/'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        numberofGust =int(request.POST.get('numberofGust', 0))
        for x in range(1,numberofGust+1):
            name=request.POST.get('text'+str(x), None)
            checked=  request.POST.get('check'+str(x), None)
            print(name,checked)
        return render(request, self.template_name,{'form': ""})


class Reporting(LoginRequiredMixin,View):
    template_name = 'chat/report.html'
    login_url ='/login/'
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        stat_time = request.POST.get('date_start', None)
        end_time = request.POST.get('date_end', None)
        membership = request.POST.get('membership', None)   
        report_type= request.POST.get('report_type', None)        
        entry= Entry.objects   
        if membership:
            entry=entry.filter(Customer__MemberNumber=membership)  
        if stat_time:
            stat_time= datetime.strptime(stat_time,'%Y-%m-%d')
            entry=entry.filter(EntryTime__date__gte=stat_time)  

        if end_time:
            end_time= datetime.strptime(end_time,'%Y-%m-%d')
            entry=entry.filter(ExitTime__date__lte=end_time)  
        entry=entry.order_by("-EntryTime")
        if report_type=='2':
            pdf = render_to_pdf('chat/report_pdf.html', {'entrys': entry})
            return HttpResponse(pdf, content_type='application/pdf')

        return render(request, self.template_name,
        {
            'entrys': entry,
            'stat_time':request.POST.get('date_start', None),
            'end_time':request.POST.get('date_end', None),
            'membership':membership
        })



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('chat/report_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



class Member(LoginRequiredMixin,View):
    template_name = 'home/member.html'
    login_url ='/login/'
    def get(self, request, *args, **kwargs):
        person = Person.objects.get(id=self.kwargs['pk'])
        categorys= ', '.join(str(cat) for cat in person.Categorys.all())
        member_entrys= Entry.objects.filter(Customer=person,ExitTime=None).order_by('-EntryTime')
        
        existing_guest=None
        allow_guest_no=settings.NUMBER_OF_ALLOW_GUEST
        if member_entrys:
            member_entrys=member_entrys[0]
            existing_guest= member_entrys.GuestEntrys.filter(ExitTime=None).all()
            # active_guest= existing_guest.filter(ExitTime=None)
            allow_guest_no=allow_guest_no - len(existing_guest)
        return render(request, self.template_name,context={"person":person,'categorys':categorys,'existing_guest':existing_guest,'allow_guest_no':allow_guest_no})

    def post(self, request, *args, **kwargs):
        numberofGust =int(request.POST.get('numberofGust', 0))
        person = Person.objects.get(id=self.kwargs['pk'])
        member_entrys= Entry.objects.filter(Customer=person,ExitTime=None).order_by('-EntryTime')
        if member_entrys and numberofGust>0:
            member_entrys=member_entrys[0]
            for x in range(1,numberofGust+1):
                name=request.POST.get('text'+str(x), None)
                CardNumber= request.POST.get('card'+str(x), None)
                checked=  request.POST.get('check'+str(x), None)
                if name:
                    if checked == 'on':
                        checked = True
                    else:
                        checked = False
                    gEntry = GuestEntry(Entry=member_entrys,EntryTime=datetime.now(),CardNumber=CardNumber , IdChecked=checked,Name=name)
                    gEntry.save()
                    member_entrys.GuestEntrys.add(gEntry)
                    member_entrys.save()
        else:
            entry = Entry(Customer=person,EntryTime=datetime.now())          
            entry.save()
            if numberofGust>0:
                for x in range(1,numberofGust+1):
                    name=request.POST.get('text'+str(x), None)
                    if name:
                        checked=  request.POST.get('check'+str(x), None)
                        cardNumber= request.POST.get('card'+str(x), None)
                        if checked == 'on':
                            checked = True
                        else:
                            checked = False
                        gEntry = GuestEntry(Entry=entry,EntryTime=datetime.now(),CardNumber=cardNumber, IdChecked=checked,Name=name)
                        gEntry.save()
                        entry.GuestEntrys.add(gEntry)
                        entry.save()
        return redirect('/')