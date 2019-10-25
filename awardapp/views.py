from django.shortcuts import render,redirect,get_object_or_404
from .models import Project,Profile,Comment,Rates
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import NewProjectForm,UpdatebioForm,CommentForm,VotesForm
from .email import send_welcome_email
from .forms import NewsLetterForm
from rest_framework.response import Response
from rest_framework.views import APIView
# from .models import  MoringaMerch
from .serializer import MerchSerializer,MerchSerializerProfile
from rest_framework import status

# display images
@login_required(login_url='/accounts/login/')
def home_images(request):
    # if request.GET.get('search_iterm'):
    #     pictures=Image.search(request.GET.get('search_iterm'))
    # else:
    pictures=Project.objects.all()
    current_user=request.user
    myprof=Profile.objects.filter(id=current_user.id).first()
    comment=Comment.objects.filter(id=current_user.id).first()
    form=NewsLetterForm
    if request.method== 'POST':
        form=NewsLetterForm(request.POST or None)
        if form.is_valid():
            name=form.cleaned_data['your_name']
            email=form.cleaned_data['email']
            recipient=NewsLetterRecipients(name=name,email=email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('home_images')
    return render(request,'index.html',{"pictures":pictures,'letterForm':form,"comment":comment,"myprof":myprof})

@login_required(login_url='/accounts/login/')
def new_image(request):
    current_user=request.user
    if request.method=='POST':
        form=NewProjectForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user=current_user
            image.save()
            # HttpResponseRedirect('hamePage')
        return redirect('homePage')
    else:
        form=NewProjectForm()
    return render(request,'registration/new_image.html',{"form":form})



@login_required(login_url='/accounts/login/')
def profilemy(request,username=None):
    current_user=request.user
    pictures=Project.objects.filter(user=current_user)
    if not username:
        username=request.user.username
        images=Project.objects.filter(title=username)
        # proc_img=Profile.objects.filter(user=current_user).first()
    return render(request,'profilemy.html',locals(),{"pictures":pictures})

@login_required(login_url='/accounts/login/')
def profile_edit(request):
    current_user=request.user
    if request.method=='POST':
        form=UpdatebioForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user=current_user
            image.save()
        return redirect('homePage')
    else:
        form=UpdatebioForm()
    return render(request,'registration/profile_edit.html',{"form":form})

def user_list(request):
    user_list=User.objects.all()
    context={'user_list':user_list}
    return render(request,'user_list.html',context)

@login_required(login_url='/accounts/login/')     
def add_comment(request,image_id):
    current_user=request.user
    image_item=Project.objects.filter(id=image_id).first()
    prof=Profile.objects.filter(user=current_user.id).first()
    if request.method=='POST':
        form=CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.posted_by=prof
            comment.comment_image=image_item
            comment.save()
            return redirect('homePage')
    else:
        form=CommentForm()
    return render(request,'comment_form.html',{"form":form,"image_id":image_id})



def search_results(request):

    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = Profile.search(search_term)
        message = f"{search_term}"

        return render(request, 'all_news/search.html',{"message":message,"users": searched_users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all_news/search.html',{"message":message})
        
@login_required(login_url='/accounts/login/') 
def likes(request,id,project_id):
    likes=1
    image=Project.objects.get(id=id)
    image.likes=image.likes+1
    image.save()
    return redirect('homePage')

@login_required(login_url='/accounts/login/') 
def projects(request,id):
    
    projects=Project.objects.filter(id=id)
    all=Rates.objects.filter(project=id)
        
    if request.method == 'POST':
        form = VotesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project =id
            rate.save()
        return redirect('projects',id)
        
    else:
        form = VotesForm() 
    
    return render(request,'one_project.html',{"projects":projects,"all":all,"form":form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = Project.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
class MerchListProfile(APIView):
    def get(self, request, format=None):
        all_merch = Profile.objects.all()
        serializers = MerchSerializerProfile(all_merch, many=True)
        return Response(serializers.data)