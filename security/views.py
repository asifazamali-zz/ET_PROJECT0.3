from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from chat.models import ChatRoom
from .models import Question,Posted_Question,Answer,Reposted_Answer
from .forms import QuestionForm,AnswerForm


###################################################################################################################################################################################
def registration_complete(request):
    return render(request,'registration/registration_complete.html',{})

def edit(request):
    print "inside edit"

    return HttpResponseRedirect('/')

def delete(request):
    quest=Question.objects.filter(id=request.POST.get('quest_id'))
    if (quest):
        quest.delete()
    print "inside delete"
    return HttpResponseRedirect('/')
def deletepost(request):
    id=request.POST.get("quest_id")
    print "deletepost quest_id",id
    post=Posted_Question.objects.get(question_id=str(id))
    post.delete()
    return HttpResponseRedirect('/')
def republish(request):
    id=request.POST.get("quest_id")
    post=Posted_Question.objects.order_by('question_id').first()
    if post:
        post.question_id=id
        post.number_of_times='2'
    else:
        post =Posted_Question(question_id=id,number_of_times='2')
    post.save()
    post.save()
    return HttpResponseRedirect('/')
def publish(request):
    id=request.POST.get("quest_id")
    print "id from form",id
    post=Posted_Question.objects.order_by('question_id').first()
    if post:
        post.question_id=id
    else:
        post =Posted_Question(question_id=id,number_of_times='1')
    post.save()
    return HttpResponseRedirect('/')
def quiz(request):
    list_a=[]
    list_b=[]
    list_c=[]
    list_d=[]
    re_list_a=[]
    re_list_b=[]
    re_list_c=[]
    re_list_d=[]
    correct=1
    form=QuestionForm(request.POST or None)
    ansform = AnswerForm(request.POST or None)
    number_of_times='0'
    _id=-1
    post=Posted_Question.objects.all()
    if(post):
        _id=post[0].question_id
        number_of_times=post[0].number_of_times

    print "id" ,_id
    switcher={
        '0':'',
        '1':'Post',
        '2':'Repost'
    }

    question=Question.objects.filter(id=_id)
    uploaded =Question.objects.all()
    submission=''
    ############################################Chat room Id Creation##########################################
    # chat=ChatRoom(name=request.user.username)
    # chat.save()
    if request.user.is_authenticated():
        model=ChatRoom.objects.filter(name=request.user.username)
        if(not model):
            create=ChatRoom(name=request.user.username)
            create.save()
                #bool,created=Question.objects.update_or_create(id=request.POST.get('id'),defaults=default_dict)
                
        # bool,created=ChatRoom.objects.update_or_create(name=request.user.username,defaults={})
        # if(bool):
        #     print "created"
    if(question):
        ques= question[0]
        print "question_id",ques.id
    else:
        ques=''
    if request.method=='POST':
        if form.is_valid():
            correct=request.POST.get('correct')
 #           print default_dict
            model=Question.objects.filter(id=int(request.POST.get('id')))
            if(model):
                model.update(question= str(request.POST.get('question')),option_a=str(request.POST.get('option_a')),
                             option_b=str(request.POST.get('option_b')),option_c=str(request.POST.get('option_c')),
                             option_d=str(request.POST.get('option_d')),option_correct=str(request.POST.get('correct')),
                            )
            else:
                instance = form.save(commit=False)
                print instance.question
                print "image",request.POST.get('image')
                instance.option_correct=correct
                #bool,created=Question.objects.update_or_create(id=request.POST.get('id'),defaults=default_dict)
                form.save()
            form=QuestionForm()
        else:
            print 'not valid'
        if ansform.is_valid():
            answer1=request.POST.get('options','')
            question_id=request.POST.get('question_id')
            repost = request.POST.get('number_of_times')
            print repost
            if(answer1):
                if repost=='1':
                    model=Answer.objects.filter(question_id=question_id).filter(user_name=request.user.username)
                    if(model):
                        model.update(answer =answer1)
                    else:
                        create=Answer(question_id=question_id,user_name=request.user.username,answer=answer1)
                        create.save()
                    #bool,created=Answer.objects.update_or_create(question_id=question_id,user_name=request.user.username,defaults={'answer':answer})
                else:
                    model=Reposted_Answer.objects.filter(question_id=question_id).filter(user_name=request.user.username)
                    if(model):
                        model.update(answer =answer1)
                    else:
                        create=Reposted_Answer(question_id=question_id,user_name=request.user.username,answer=answer1)
                    # if(model):Answer(question_id=question_id,user_name=request.user.username,answer=answer)
                        create.save()
                #bool,created=Reposted_Answer.objects.update_or_create(question_id=question_id,user_name=request.user.username,defaults={'answer':answer})

                ques    =''
                submission='Your answer has submitted!!'
    if question:
        correct=Question.objects.filter(id=_id)[0].option_correct
    option_a=Answer.objects.filter(answer='0').filter(question_id=_id)
    for l in option_a:
        list_a.append(str(l.user_name))
    option_b=Answer.objects.filter(answer='1').filter(question_id=_id)
    for l in option_b:
        list_b.append(str(l.user_name))

    option_c=Answer.objects.filter(answer='2').filter(question_id=_id)
    for l in option_c:
        list_c.append(str(l.user_name))

    option_d=Answer.objects.filter(answer='3').filter(question_id=_id)
    for l in option_d:
        list_d.append(str(l.user_name))
    repost_a=Reposted_Answer.objects.filter(answer='0').filter(question_id=_id)
    for l in repost_a:
        re_list_a.append(str(l.user_name))
    repost_b=Reposted_Answer.objects.filter(answer='1').filter(question_id=_id)
    for l in repost_b:
        re_list_b.append(str(l.user_name))

    repost_c=Reposted_Answer.objects.filter(answer='2').filter(question_id=_id)
    for l in repost_c:
        re_list_c.append(str(l.user_name))

    repost_d=Reposted_Answer.objects.filter(answer='3').filter(question_id=_id)
    for l in repost_d:
        re_list_d.append(str(l.user_name))
    return render_to_response(
    'quiz.html',
    {'request':request,'form':form,'ques':ques,'submission':submission,'uploaded':uploaded,
     'post':switcher[number_of_times],'number_of_times':number_of_times,'option_a':len(list_a),'option_b':len(list_b),
        'option_c':len(list_c),'option_d':len(list_d),'re_option_a':len(re_list_a),'re_option_b':len(re_list_b),
        're_option_c':len(re_list_c),'re_option_d':len(re_list_d),'correct':correct},
        context_instance=RequestContext(request))




