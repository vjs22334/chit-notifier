from django.shortcuts import render,redirect
from .forms import *
from .models import *
from .excel_reader import *
from .selenium_whatsappweb import *

# Create your views here.

def home(request):
    return render(request,'home.html')



def WhatsAppReport(request):
    if request.GET.get('clear',False):
        messages = WhatsappMessagesToSend.objects.all()
        for message in messages:
            WhatsAppLogs(name = message.name,status = message.status,group = message.group).save()
        WhatsappMessagesToSend.objects.all().delete()
        return redirect(sendWhatsapp)
    else:
        import pdb; pdb.set_trace()
        successMessages = WhatsappMessagesToSend.objects.filter(status = "5")
        failedMessages = WhatsappMessagesToSend.objects.exclude(status = "5")
        return render(request,"whatsAppReport.html",{
            "successMessages":successMessages,
            "failedMessages":failedMessages,
            "cleared": False
        })


def SendWhatsappMessages(request):
    #import pdb; pdb.set_trace()
    if WhatsappMessagesToSend.objects.all().count()!=0:

        successful = WhatsappMessagesToSend.objects.filter(status = "5")
        for message in successful:
            WhatsAppLogs(name = message.name,status = message.status,group = message.group).save()
            message.delete()


        namemissing = WhatsappMessagesToSend.objects.filter(status = "1")
        for message in namemissing:
            if userDetails.objects.filter(name = message.name).exists():
                message.status = "2"
                message.save()
        
        
        
        filemissing = WhatsappMessagesToSend.objects.filter(status = "2")
        for message in filemissing:
            path = get_file(join(BASE_DIR,"testfiles"),message.name+"_"+message.group+".pdf")
            if path!="":
                message.status = "4"
                message.path = path
                message.save()

            
        
        try:
            recepients = []
            messagesToSend = WhatsappMessagesToSend.objects.filter(status = "4")
            for message in messagesToSend:
                user = userDetails.objects.get(name = message.name)
                if user.whatsapp_number:
                    recepients.append({
                        "name":message.name,
                        "number":user.whatsapp_number,
                        "path":message.path,
                    })
                else:
                    message.status = 3
                    message.save()
            send_messages(recepients)
        except Exception as e:
            print("exception:"+str(e))
            pass
            #do nothing
    
    return redirect(WhatsAppReport)
            




def sendWhatsapp(request):

    if WhatsappMessagesToSend.objects.all().count()!=0:
        return redirect(WhatsAppReport)

    if request.method=="POST":
        #import pdb; pdb.set_trace()
        messageform = MessageForm(request.POST or None)
        if 'usernames' in request.POST:
            usernamesform = UserNamesForm(request.POST or None)
            if messageform.is_valid() and usernamesform.is_valid():
                messageform.save()
                usernames =  usernamesform.cleaned_data['usernames']
                groupno = usernamesform.cleaned_data['group_no']
                #check for files and add to whatsapp messages to send
                for username in usernames:
                    path = get_file(join(BASE_DIR,"testfiles"),username+"_"+groupno+".pdf")
                    if messageform.cleaned_data['attach_pdf']:
                        if path!="":
                            m = WhatsappMessagesToSend(name = username,path = path,status = "4",group = groupno)
                            m.save()
                        else:
                            m = WhatsappMessagesToSend(name = username,path = path,status = "2",group = groupno)
                            m.save()
                    else:
                        m = WhatsappMessagesToSend(name = username,path = "",status = "4",group = groupno)
                        m.save()
                #call function to send whats app messages      
                #return redirect to reports page
                return redirect(SendWhatsappMessages)

        else:
            if messageform.is_valid():
                messageform.save()
                files =  get_files(join(BASE_DIR,'testfiles'),"xls")
                # import pdb; pdb.set_trace()
                for f in files:
                    (sheetX,groupno) = clean(f)
                    for username in sheetX["Subscriber Name"]:
                        if not userDetails.objects.filter(name = username).exists():
                            m = WhatsappMessagesToSend(name = username,path = "",status = "1",group = groupno)
                            m.save()

                        else:
                            path = get_file(join(BASE_DIR,"testfiles"),username+"_"+groupno+".pdf")
                            if messageform.cleaned_data['attach_pdf']:
                                if path!="":
                                    m = WhatsappMessagesToSend(name = username,path = path,status = "4",group = groupno)
                                    m.save()
                                else:
                                    m = WhatsappMessagesToSend(name = username,path = path,status = "2",group = groupno)
                                    m.save()
                            else:
                                m = WhatsappMessagesToSend(name = username,path = "",status = "4",group = groupno)
                                m.save()
             #call function to send whats app messages      
                #return redirect to reports page
                return redirect(SendWhatsappMessages)
            else:
                usernamesform = UserNamesForm()
    else:
        if len(Message.objects.filter(message_type = "1" )) != 0:
            message = Message.objects.filter(message_type = "1" )[0]
            messageform = MessageForm(instance = message)
        else:
            messageform = MessageForm()
        usernamesform = UserNamesForm()

    return render(request,'sendMessage.html',{
        'messageform':messageform,
        'usernamesform':usernamesform,
        })