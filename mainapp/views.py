from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Group_account,User_account,User_history,Schedule, Invite,Punish,Group_history
from django.conf import settings
from datetime import datetime, timezone, timedelta
from django.utils import timezone
def index(request):
    return render(request, 'index.html')


def login(request):
    auth.logout(request)
    return render(request, 'login.html')


def portfolio(request):
    users = User_account.objects.all()

    if request.method == 'POST':
        us = User_account()
        us.name = request.user
        us.user_money = 0
        us.nickname = request.POST['nickname']
        if bool(request.FILES.get('image',False)) == True:
            us.image = request.FILES['image']
        us.save()
        
        return redirect('/home')
    else:
        for user in users:
            if user.name.username == request.user.username:
                return redirect('/home')
                break
        return render(request, 'portfolio.html')


def home(request):
    users = User_account.objects.all()
    groups = Group_account.objects.all()
    us = User_account()
    user_group= []
    
    for user in users:
        if user.name.username == request.user.username:
            us = User_account.objects.get(name = request.user)
            break

    for group in groups:
        for member in group.members.all():
            if member.name.username == request.user.username:
                user_group.append(group)

    nickname = User_account.objects.get(name = request.user)
    punishs= Punish.objects.filter(nick=nickname).values('schedule_id')
    sche = []
    first = []
    for key in punishs.all():
        sche.append(Schedule.objects.get(pk = key['schedule_id']))
    
    sche.sort(key=lambda r:r.date)
    
    if not sche:
        pass
    else: 
        first=sche.pop(0)
        first.date += timedelta(hours=9)

    return render(request, 'home.html',{'groups': user_group,'us':us, 'first':first})

    
def invite(request):
    users = User_account.objects.all() 
    us = User_account.objects.get(name = request.user)
    groups = Group_account.objects.all()
    group = Group_account()
    invitation = Invite()
    invitations = Invite.objects.all()
    us_f_list = []
    cnt = 0
    cnt_list =[]
    check = 0


    if request.method == 'POST':
                
        ############### 동일한 그룹이면 같은멤버 (수정해야함)##############
        for grp in groups:
            cnt_list.append(grp)
            if grp.title != request.POST['gr']:
                cnt += 1

        if cnt == len(cnt_list):
            group.title = request.POST['gr']
            group.save()
            group.members.add(us)
            group.save()
        else:
            group = Group_account.objects.get(title=request.POST['gr'])
        ################################################################
        
        ######################## 초대장 만들기 ##########################
        invitation.title = request.POST['gr']
        invitation.send = us.nickname
        invitation.receive = request.POST['invite']
        invitation.save()
        
        for i in invitations: # 초대장 같은 객체 중복생성 불가
            if i.receive == request.POST['invite'] and i.send == us.nickname and i.title == request.POST['gr']:
                check+=1
                if check != 1:
                    i.delete()
        #################################################################

        invitations_i = Invite.objects.all() # 최종 초대장
        

        for iv in invitations_i:
            if iv.title == request.POST['gr'] and iv.send == us.nickname: # 초대장의 title과 검색한 title이 같으면
                us_f = User_account.objects.get(nickname = iv.receive)
                us_f_list.append(us_f)
                

        return render(request, 'invite.html', {'us_f_list':us_f_list,'group':group})

    else:
        return render(request, 'invite.html')



def search(request):
    group = request.POST['gr']
    if request.method == 'POST':
        us = User_account.objects.get(name = request.user)
        us_m = User_account.objects.get(nickname=request.POST['invite'])
        member = request.POST['invite']
        us_f_list = []

        users = User_account.objects.all()

        invitations_i = Invite.objects.all() # 최종 초대장
        

        if not invitations_i:
            pass
        else:
            for iv in invitations_i:
                if iv.title == request.POST['gr'] and iv.send == us.nickname: # 초대장의 title과 검색한 title이 같으면
                    us_f = User_account.objects.get(nickname = iv.receive)
                    us_f_list.append(us_f)
            

        return render(request, 'search.html', {'us_m':us_m, 'group':group, 'member':member, 'us_f_list':us_f_list})
    return render(request, 'search.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')


def group(request,group_id):
    group = get_object_or_404(Group_account, pk=group_id)
    sche= Schedule.objects.filter(group_ac = group)
    history = Group_history.objects.filter( g = group).order_by('-id')
    return render(request, 'group.html',{'group' : group, 'schedules': sche, 'histories':history})


def newSchedule(request,group_id): 
    group = get_object_or_404(Group_account,pk=group_id)
    return render(request, 'newSche.html',{'group' : group})

def create(request,group_id):
    schedule = Schedule()
    schedule.group_ac = get_object_or_404(Group_account, pk = group_id)
    schedule.title = request.GET['title']
    schedule.penalty = request.GET['penalty']
    schedule.date = request.GET['date']+" "+request.GET['time']
    schedule.save()

    for group_user in schedule.group_ac.members.all():
        group_user.user_money = group_user.user_money - int(schedule.penalty)
        schedule.group_ac.group_money += int(schedule.penalty)
        punish = Punish()
        punish.nick = group_user.nickname
        punish.success = False
        punish.schedule = schedule
        punish.save()
    
    schedule.group_ac.save()
    group_user.save()

    return redirect('/group/'+str(schedule.group_ac.id))


def check(request):
    inv_list=[]
    invitations = Invite.objects.all()
    us = User_account.objects.get(name = request.user)

    for inv in invitations:
        if inv.receive == us.nickname:
            inv_list.append(inv)


    
    return render(request, 'check.html', {'inv_list':inv_list})


def yes(request, inv_id):
    us = User_account.objects.get(name = request.user)
    invi_us = get_object_or_404(Invite, pk=inv_id)
    invi_us.check = True
    invi_us.save()
    group = Group_account.objects.get(title = invi_us.title)
    group.title = invi_us.title
    group.save()
    group.members.add(us)
    group.save()
    invi_us.delete()
    
    return redirect('/home')


def no(request):
    
    return redirect('/home')


def logout(request):
    auth.logout(request)
    return redirect('/login')



def delete(request):
    user_id = request.POST['user_id']
    us = get_object_or_404(User_account, pk=user_id)
    invites = Invite.objects.all()
    use = User_account.objects.get(name = request.user)

    for iv in invites:
        if iv.receive == us.nickname and iv.send == use.nickname:
            iv.delete()
            break 
    return redirect('/invite')
    
def map(request):
    nickname = User_account.objects.get(name = request.user)
    punishs= Punish.objects.filter(nick=nickname).values('schedule_id')
    sche = []
    first = []
    for key in punishs.all():
        sche.append(Schedule.objects.get(pk = key['schedule_id']))
    
    sche.sort(key=lambda r:r.date)
    
    if not sche:
        return render(request, 'map2.html')
    else: 
        first=sche.pop(0)
        first.date += timedelta(hours=9)
        return render(request, 'map.html', {'schedule':sche, 'first':first})
    



def confirm(request,first_id):
    sch = get_object_or_404(Schedule, pk = first_id)
    nickname = User_account.objects.get( name = request.user)
    punish= Punish.objects.filter(schedule= sch).get(nick= nickname)
    timenow = datetime.now()
    timesche = datetime(sch.date.year, sch.date.month, sch.date.day, sch.date.hour, sch.date.minute, sch.date.second)
    t = (timesche+timedelta(hours=9))-timenow 
    if t > timedelta(hours=0) :
        punish.success = True
        punish.save()
        nickname.user_money += int(sch.penalty)
        sch.group_ac.group_money -= int(sch.penalty)
        sch.group_ac.save()
        nickname.save()
        return redirect('/home')
    else:
        return redirect('/map')

def scheDelete(request , first_id):
    sche = get_object_or_404(Schedule, pk = first_id)
    punishs = Punish.objects.filter(schedule = sche)
    
    for punish in punishs.all() :
        if punish.success == False:
            history = Group_history()
            history.name = sche.title
            history.date = sche.date
            history.money = sche.penalty
            history.us = punish.nick
            history.g = sche.group_ac
            history.save()

    sche.delete()
    return redirect('/home')

def charge(request, user_id):
    user = get_object_or_404(User_account, pk = user_id)
    user.user_money +=10000
    user.save()
    return redirect('/home')