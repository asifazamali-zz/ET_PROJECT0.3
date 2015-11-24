from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from chat.models import ChatRoom
from security.models import Answer,Posted_Question,Question,Reposted_Answer
import json
import random
import random
import math

def assignment(l,correct):
    a_len=len(l[0])
    b_len=len(l[1])
    c_len=len(l[2])
    d_len=len(l[3])
    allocated=[]

    correct_len=len(l[correct])
    len_of_correct= correct_len
    total=float(a_len+b_len+c_len+d_len-correct_len)
    s = a_len+b_len+c_len+d_len
    switcher ={
	a_len: l[0],
	b_len: l[1],
	c_len: l[2],
	d_len: l[3],
	}
    check=switcher.get(s,False)
    if(check):
	    return [check]
    if not total:
        return
    a_ratio=(a_len/total)
    #print a_ratio
    b_ratio=(b_len/total)
    c_ratio=(c_len/total)
    d_ratio=(d_len/total)

    allocated_index=[]
    final_allocation = []
    if correct==0:
	    i=0
	    #allocated = []
	    #allocated_index.append(index_list)
	    #print correct_len
	    allocated_to_b=int(math.ceil(b_ratio*correct_len))
	    correct_len -= allocated_to_b
	    #print correct_len
	    print total
	    #print a_ratio/float(total)
	    allocated_to_c=int(math.ceil(c_ratio*correct_len))
	    correct_len -= allocated_to_c
	    #print correct_len
	    allocated_to_d=correct_len
	    #print correct_len
	    print allocated_to_b+allocated_to_c+allocated_to_d
	    index_list=[]
	    if allocated_to_b>0:
		index_list = random.sample(range(0,b_len),allocated_to_b if (int(total)>len_of_correct) else b_len)
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[1][index],l[correct][i]])  ########random allocation of l[correct] to l[1]
	 	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_b"
	    print allocated_index
	    print "final_allocation_b"
	    print final_allocation
	    #final_allocation.append(allocated)
	    allocated = []
	    index_list=[]
	    allocated_index.append(index_list)
	    if allocated_to_c>0:
		index_list = random.sample(range(0,c_len),allocated_to_c if (int(total)>len_of_correct) else c_len)
		print "index_list_c"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[2][index],l[correct][i]])   ########random allocation of l[correct] to l[2]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_c"
	    print allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_c"
	    print final_allocation
	    allocated = []
	    index_list=[]
	    # print l[3]
	    print allocated_to_d
	    if allocated_to_d>0:
		index_list = random.sample(range(0,d_len),allocated_to_d if (int(total)>len_of_correct) else d_len)
		print "index_list"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[3][index],l[correct][i]])  ########random allocation of l[correct] to l[3]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_d",allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_d",final_allocation
	    total_list=[range(0,a_len),range(0,b_len),range(0,c_len),range(0,d_len)]
	    j=0
	    final_result=[]
	    while(j<len(total_list)):					 ###########final_result=l[total]-l[allocated_index]
		result=[]
		for item in total_list[j]:
		    #print allocated_index
		    if(j==correct):
		    	if item not in range(0,i):
		   		result.append(item)
		    else:
		    	if item not in allocated_index[j]:
		        	result.append(item)
		j=j+1
		final_result.append(result)
	    print "final_unallocated_list"
	    print final_result
	    print final_allocation
	    i=0
	    j=0
	    while(j< len(final_result[1])):				############### mapping l[1] to l[2]
		    if final_result[2]:
		        final_allocation.append([l[1][final_result[1][j]],l[2][final_result[2][i]]])
		        final_result[2].pop(i)
		        final_result[1].pop(j)
		    else:
			if final_result[3]:				############ if l[2] ends map it to l[3]
				i=0
				final_allocation.append([l[1][final_result[1][j]],l[3][final_result[3][i]]])
				final_result[3].pop(i)
				final_result[1].pop(j)
			else:						############ if l[1] remains append to final_allocation serially
				k=0
				while(j<len(final_result[1])):
					final_allocation[k].append(l[1][final_result[1][j]])
					final_result[1].pop(j)
					k=(k+1)%len(final_allocation)
		#print final_allocation[0]
	    #if final_result[1]:
	    #	    k = 0;
	    #	    for b in final_result[1]:
	    #	        final_allocation[k].append(l[1][b])
	    #		k+=1
	    print final_allocation
	    print final_result
	    while(j<len(final_result[2])):                                     ########### map l[2] to l[3]
		    if final_result[3]:
			final_allocation.append([l[2][final_result[2][j]],l[3][final_result[3][i]]])
			final_result[3].pop(i)
			final_result[2].pop(j)
		    else:
			k=0
			for item in final_result[2]:				######## remaining l[2] to append in final_allocation
				final_allocation[k].append(l[2][final_result[2][j]])
				final_result[2].pop(j)
				k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[3])):					########### remaining l[3] to append in final_allocation
			final_allocation[k].append(l[3][final_result[3][j]])
			final_result[3].pop(j)
			k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[correct])):				########## map remaining l[correct] to append in final_allocation
			final_allocation[k].append(l[correct][final_result[correct][j]])
			final_result[correct].pop(j)
			k=(k+1)%len(final_allocation)
    if correct==1:
	    i=0
	    #allocated = []
	    #allocated_index.append(index_list)
	    #print correct_len
	    allocated_to_a=int(math.ceil(a_ratio*correct_len))
	    correct_len -= allocated_to_a
	    #print correct_len
	    print total
	    #print a_ratio/float(total)
	    allocated_to_c=int(math.ceil(c_ratio*correct_len))
	    correct_len -= allocated_to_c
	    #print correct_len
	    allocated_to_d=correct_len
	    #print correct_len
	    print allocated_to_a+allocated_to_c+allocated_to_d
	    index_list=[]
	    if allocated_to_a>0:
		index_list = random.sample(range(0,a_len),allocated_to_a if (int(total)>len_of_correct) else a_len)
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[0][index],l[correct][i]]) ########random allocation of l[correct] to l[0]
	 	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_a"
	    print allocated_index
	    print "final_allocation_a"
	    print final_allocation
	    #final_allocation.append(allocated)
	    allocated = []
	    index_list=[]
	    allocated_index.append(index_list)
	    if allocated_to_c>0:
		#print "allocated_to_c",allocated_to_c,total,int(total)>correct_len
		index_list = random.sample(range(0,c_len),allocated_to_c if (int(total)>len_of_correct) else c_len)
		print "index_list_c"
		print index_list
		i=0
		for index in index_list:
		    print index,l[1][i]
		    final_allocation.append([l[2][index],l[correct][i]])   ########random allocation of l[correct] to l[2]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_c"
	    print allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_c"
	    print final_allocation
	    allocated = []
	    index_list=[]
	    # print l[3]
	    print allocated_to_d
	    if allocated_to_d>0:
		index_list = random.sample(range(0,d_len),allocated_to_d if (int(total)>len_of_correct) else d_len)
		print "index_list"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[3][index],l[correct][i]])  ########random allocation of l[correct] to l[3]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_d",allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_d",final_allocation
	    total_list=[range(0,a_len),range(0,b_len),range(0,c_len),range(0,d_len)]
	    j=0
	    final_result=[]
	    while(j<len(total_list)):      ##########final_result=l[total]-l[allocated_index]
		result=[]
		for item in total_list[j]:
		    #print allocated_index
		    if(j==1):
		    	if item not in range(0,i):
		   		result.append(item)
		    else:
		    	if item not in allocated_index[j]:
		        	result.append(item)
		j=j+1
		final_result.append(result)
	    print "final_unallocated_list"
	    print final_result
	    print final_allocation
	    i=0
	    j=0
	    while(j< len(final_result[0])):                    ############### mapping l[0] to l[2]
		    if final_result[2]:
		        final_allocation.append([l[0][final_result[0][j]],l[2][final_result[2][i]]])
		        final_result[2].pop(i)
		        final_result[0].pop(j)
		    else:
			if final_result[3]:			############ if l[2] ends map it to l[3]
				i=0
				final_allocation.append([l[0][final_result[0][j]],l[3][final_result[3][i]]])
				final_result[3].pop(i)
				final_result[0].pop(j)
			else:					############ if l[0] remains append to final_allocation serially
				k=0
				while(j<len(final_result[0])):
					final_allocation[k].append(l[0][final_result[0][j]])
					final_result[0].pop(j)
					k=(k+1)%len(final_allocation)
		#print final_allocation[0]
	    #if final_result[0]:
	    #	    k = 0;
	    #	    for a in final_result[0]:
	    #	        final_allocation[k].append(l[0][a])
	    #		k+=1
	    print final_allocation
	    print final_result
	    while(j<len(final_result[2])):		########### map l[2] to l[3]
		    if final_result[3]:
			final_allocation.append([l[2][final_result[2][j]],l[3][final_result[3][i]]])
			final_result[3].pop(i)
			final_result[2].pop(j)
		    else:
			k=0
			for item in final_result[2]:
				final_allocation[k].append(l[2][final_result[2][j]])    ######## remaining l[2] to append in final_allocation
				final_result[2].pop(j)
				k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[3])):						########### remaining l[3] to append in final_allocation

			final_allocation[k].append(l[3][final_result[3][j]])
			final_result[3].pop(j)
			k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[1])):					########## map remaining l[correct] to append in final_allocation
			final_allocation[k].append(l[1][final_result[1][j]])
			final_result[1].pop(j)
			k=(k+1)%len(final_allocation)
    if correct==2:
	    i=0
	    #allocated = []
	    #allocated_index.append(index_list)
	    #print correct_len
	    allocated_to_a=int(math.ceil(a_ratio*correct_len))
	    correct_len -= allocated_to_a
	    #print correct_len
	    print total
	    #print a_ratio/float(total)
	    allocated_to_b=int(math.ceil(b_ratio*correct_len))
	    correct_len -= allocated_to_b
	    #print correct_len
	    allocated_to_d=correct_len
	    #print correct_len
	    print allocated_to_a+allocated_to_b+allocated_to_d
	    index_list=[]
	    if allocated_to_a>0:
		index_list = random.sample(range(0,a_len),allocated_to_a if (int(total)>len_of_correct) else a_len)
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[0][index],l[correct][i]])   ########random allocation of l[correct] to l[0]
	 	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_a"
	    print allocated_index
	    print "final_allocation_a"
	    print final_allocation
	    #final_allocation.append(allocated)
	    allocated = []
	    index_list=[]
	    allocated_index.append(index_list)
	    if allocated_to_b>0:
		index_list = random.sample(range(0,b_len),allocated_to_b if (int(total)>len_of_correct) else b_len)
		print "index_list_"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[1][index],l[correct][i]])	########random allocation of l[correct] to l[1]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_c"
	    print allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_c"
	    print final_allocation
	    allocated = []
	    index_list=[]
	    # print l[3]
	    print allocated_to_d
	    if allocated_to_d>0:
		index_list = random.sample(range(0,d_len),allocated_to_d if (int(total)>len_of_correct) else d_len)

		print "index_list"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[3][index],l[correct][i]])	########random allocation of l[correct] to l[3]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_d",allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_d",final_allocation
	    total_list=[range(0,a_len),range(0,b_len),range(0,c_len),range(0,d_len)]
	    j=0
	    final_result=[]
	    while(j<len(total_list)):		###########final_result=l[total]-l[allocated_index]
		result=[]
		for item in total_list[j]:
		    #print allocated_index
		    if(j==correct):
		    	if item not in range(0,i):
		   		result.append(item)
		    else:
		    	if item not in allocated_index[j]:
		        	result.append(item)
		j=j+1
		final_result.append(result)
	    print "final_unallocated_list"
	    print final_result
	    print final_allocation
	    i=0
	    j=0
	    while(j< len(final_result[0])):
		    if final_result[1]:
		        final_allocation.append([l[0][final_result[0][j]],l[1][final_result[1][i]]])############### mapping l[0] to l[1]
		        final_result[1].pop(i)
		        final_result[0].pop(j)
		    else:
			if final_result[3]:						############ if l[1] ends map it to l[3]
				i=0
				final_allocation.append([l[0][final_result[0][j]],l[3][final_result[3][i]]])
				final_result[3].pop(i)
				final_result[0].pop(j)
			else:							############ if l[0] remains append to final_allocation serially
				k=0
				while(j<len(final_result[0])):
					final_allocation[k].append(l[0][final_result[0][j]])
					final_result[0].pop(j)
					k=(k+1)%len(final_allocation)
		#print final_allocation[0]
	    #if final_result[0]:
	    #	    k = 0;
	    #	    for a in final_result[0]:
	    #	        final_allocation[k].append(l[0][a])
	    #		k+=1
	    print final_allocation
	    print final_result
	    while(j<len(final_result[1])):		########### map l[1] to l[3]
		    if final_result[3]:
			final_allocation.append([l[1][final_result[1][j]],l[3][final_result[3][i]]])
			final_result[3].pop(i)
			final_result[1].pop(j)
		    else:
			k=0
			for item in final_result[1]:			######## remaining l[2] to append in final_allocation
				final_allocation[k].append(l[1][final_result[1][j]])
				final_result[1].pop(j)
				k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[3])):
			final_allocation[k].append(l[3][final_result[3][j]])  ########### remaining l[3] to append in final_allocation
			final_result[3].pop(j)
			k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[correct])):				########## map remaining l[correct] to append in final_allocation
			final_allocation[k].append(l[correct][final_result[correct][j]])
			final_result[correct].pop(j)
			k=(k+1)%len(final_allocation)
    if correct==3:
	    i=0
	    #allocated = []
	    #allocated_index.append(index_list)
	    #print correct_len
	    allocated_to_a=int(math.ceil(a_ratio*correct_len))
	    correct_len -= allocated_to_a
	    #print correct_len
	    print total
	    #print a_ratio/float(total)
	    allocated_to_b=int(math.ceil(b_ratio*correct_len))
	    correct_len -= allocated_to_b
	    #print correct_len
	    allocated_to_c=correct_len
	    #print correct_len
	    print allocated_to_a+allocated_to_b+allocated_to_c
	    index_list=[]
	    if allocated_to_a>0:
		index_list = random.sample(range(0,a_len),allocated_to_a if (int(total)>len_of_correct) else a_len)
		i=0
		for index in index_list:
		    final_allocation.append([l[0][index],l[correct][i]])   ########random allocation of l[correct] to l[0]
	 	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_a"
	    print allocated_index
	    print "final_allocation_a"
	    print final_allocation
	    #final_allocation.append(allocated)
	    allocated = []
	    index_list=[]
	    allocated_index.append(index_list)
	    if allocated_to_b>0:
		#print "allocated_to_c",allocated_to_c,total,int(total)>correct_len
		index_list = random.sample(range(0,b_len),allocated_to_b if (int(total)>len_of_correct) else b_len)
		print "index_list_b"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[1][index],l[correct][i]]) ########random allocation of l[correct] to l[2]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_b"
	    print allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_b"
	    print final_allocation
	    allocated = []
	    index_list=[]
	    # print l[3]
	    print allocated_to_c
	    if allocated_to_c>0:
		index_list = random.sample(range(0,c_len),allocated_to_c if (int(total)>len_of_correct) else c_len)
		print "index_list"
		print index_list
		i=0
		for index in index_list:
		    final_allocation.append([l[2][index],l[correct][i]])	########random allocation of l[correct] to l[2]
	    	    i+=1
	    allocated_index.append(index_list)
	    print "allocated_index_c",allocated_index
	    #final_allocation.append(allocated)
	    print "final_allocation_d",final_allocation
	    total_list=[range(0,a_len),range(0,b_len),range(0,c_len),range(0,d_len)]
	    j=0
	    final_result=[]
	    while(j<len(total_list)):			###########final_result=l[total]-l[allocated_index]
		result=[]
		for item in total_list[j]:
		    #print allocated_index
		    if(j==correct):
		    	if item not in range(0,i):
		   		result.append(item)
		    else:
		    	if item not in allocated_index[j]:
		        	result.append(item)
		j=j+1
		final_result.append(result)
	    print "final_unallocated_list"
	    print final_result
	    print final_allocation
	    i=0
	    j=0
	    while(j< len(final_result[0])):
		    if final_result[1]:			############### mapping l[0] to l[1]
		        final_allocation.append([l[0][final_result[0][j]],l[1][final_result[1][i]]])
		        final_result[1].pop(i)
		        final_result[0].pop(j)
		    else:
			if final_result[2]:		############ if l[1] ends map it to l[2]
				i=0
				final_allocation.append([l[0][final_result[0][j]],l[2][final_result[2][i]]])
				final_result[2].pop(i)
				final_result[0].pop(j)
			else:
				k=0			############ if l[1] remains append to final_allocation serially
				while(j<len(final_result[0])):
					final_allocation[k].append(l[0][final_result[0][j]])
					final_result[0].pop(j)
					k=(k+1)%len(final_allocation)
		#print final_allocation[0]
	    #if final_result[0]:
	    #	    k = 0;
	    #	    for a in final_result[0]:
	    #	        final_allocation[k].append(l[0][a])
	    #		k+=1
	    print final_allocation
	    print final_result
	    while(j<len(final_result[1])):           ########### map l[1] to l[2]
		    if final_result[2]:
			final_allocation.append([l[1][final_result[1][j]],l[2][final_result[2][i]]])
			final_result[2].pop(i)
			final_result[1].pop(j)
		    else:
			k=0
			for item in final_result[1]:		######## remaining l[1] to append in final_allocation
				final_allocation[k].append(l[1][final_result[1][j]])
				final_result[1].pop(j)
				k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[2])):			########### remaining l[2] to append in final_allocation
			final_allocation[k].append(l[2][final_result[2][j]])
			final_result[2].pop(j)
			k=(k+1)%len(final_allocation)
	    k=0
	    while(j<len(final_result[3])):
			final_allocation[k].append(l[3][final_result[3][j]])  ########## map remaining l[correct] to append in final_allocation
			final_result[3].pop(j)
			k=(k+1)%len(final_allocation)

    print "at last"
    print l
    print final_result
    return final_allocation







def index(request):
    chat_rooms = ChatRoom.objects.order_by('name')[:5]
    context = {
        'chat_list': chat_rooms,
    }
    return render(request,'chats/index.html', context)

def chat_room(request):
    list_a=[]
    list_b=[]
    list_c=[]
    list_d=[]
    re_list_a=[]
    re_list_b=[]
    re_list_c=[]
    re_list_d=[]
    correct=1
    _id=''
    posted=Posted_Question.objects.all()
    if posted:
        _id=posted[0].question_id
        print 'id',_id
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
    print "inside views",[list_a,list_b,list_c,list_d],correct
    print [re_list_a,re_list_b,re_list_c,re_list_d],correct
    output = assignment([list_a,list_b,list_c,list_d],int(correct))
    print "output from assignment",output
    #chat = get_object_or_404(ChatRoom, pk=request.user.pk)
    if output:
        #if (len(output)==1):
        #    list=json.dumps([output])
        #else:
            list=json.dumps(output)
    else:
        list=[[],[],[],[]]
    #print list
    return render(request, 'chats/chat_room.html', {'list':list,'question_id':_id})

def longpoll_chat_room(request, chat_room_id):
    chat = get_object_or_404(ChatRoom, pk=chat_room_id)
    return render(request, 'chats/longpoll_chat_room.html', {'chat': chat},)
