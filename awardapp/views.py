from django.shortcuts import render,redirect,get_object_or_404
from .models import Project,Profile,Comment
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import NewProjectForm,UpdatebioForm,CommentForm
from .email import send_welcome_email
from .forms import NewsLetterForm
# from .forms import NewArticleForm, NewsLetterForm

# @login_required(login_url='/accounts/login/')
# def home_images(request):
#     return render(request,'index.html')

# from django.http  import HttpResponse

# Create your views here.
# def home_images(request):
#     return HttpResponse('Welcome to the Moringa Tribune')

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
def likes(request,id):
    likes=1
    image=Project.objects.get(id=id)
    image.likes=image.likes+1
    image.save()
    return redirect('homePage')

@login_required(login_url='/accounts/login/') 
def projects(request,id):
    
    projects=Project.objects.filter(id=id)
    
    try:

        
        all = Rates.objects.filter(project=project_id) 
        print(all)
    except Exception as e:
        raise Http404() 
    
    # single user votes count
    count = 0
    for i in all:
        count+=i.usability
        count+=i.design
        count+=i.content
    
    if count > 0:
        average = round(count/3,1)
    else:
        average = 0
        
    if request.method == 'POST':
        form = VotesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project_id
            rate.save()
        return redirect('projects',project_id)
        
    else:
        form = VotesForm() 
        
    # The votes logic
    votes = Rates.objects.filter(project=project_id)
    usability = []
    design = []
    content = [] 
    
    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content) 
        
    if len(usability) > 0 or len(design)>0 or len(content)>0:
        average_usability = round(sum(usability)/len(usability),1) 
        average_design = round(sum(design)/len(design),1)
        average_content = round(sum(content)/len(content),1) 
            
        average_rating = round((average_content+average_design+average_usability)/3,1) 
    
    else:
        average_content=0.0
        average_design=0.0
        average_usability=0.0
        average_rating = 0.0
        
    '''
    To make sure that a user only votes once
    '''
    
    arr1 = []
    for use in votes:
        arr1.append(use.user_id) 
                
    auth = arr1
       
    reviews = ReviewForm(request.POST)
    if request.method == 'POST':
        
        if reviews.is_valid():
            comment = reviews.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect ('projects',project_id)
        else:
            reviews = ReviewForm()
            
        
    user_comments = Comments.objects.filter(pro_id=project_id)
       
    # context = {
    #     'projects':projects,
    #     'form':form,
    #     'usability':average_usability,
    #     'design':average_design,
    #     'content':average_content,
    #     'average_rating':average_rating,
    #     'auth':auth,
    #     'all':all,
    #     'average':average,
    #     'comments':user_comments,
    #     'reviews':reviews,
        
    # }
    
    # return render(request,'single_post.html',context) 
    return render(request,'one_project.html',{"projects":projects,"form":form,"usability":average_usability,"design":average_design,"content":average_content,"average_rating":average_rating,"auth":auth,"all":all,
    "average":average,"comments":user_comments,"reviews":reviews})
