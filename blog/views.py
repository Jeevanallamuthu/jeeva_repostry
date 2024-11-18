from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging 
from .models import Post,AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm 

#posts=[
#       {'id':1,'title':'post 1','content':'content of post 1'},
 #       {'id':2,'title':'post 2','content':'content of post 2'},
  ##      {'id':3,'title':'post 3','content':'content of post 3'},
    #    {'id':4,'title':'post 4','content':'content of post 4'},
    #]

# Create your views here.
def index(request):
    blog_title="Latest posts"
    #getting data from post model
    all_posts=Post.objects.all()
    #paginate
    paginator=Paginator(all_posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request,'blog/index.html',{'blog_title':blog_title,'page_obj':page_obj})

def detail(request,slug):
    #getting static data
    #post=next((item for item in posts if item ['id']==int(post_id)),None)

    try:
        #getting data from model by post id
        post=Post.objects.get(slug=slug)
        related_posts=Post.objects.filter(category=post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does not Exists!")


    #logger=logging.getLogger("TESTING")
    #logger.debug(f'post variable is {post}')
    return render(request,'blog/detail.html',{'post':post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("this is new url page")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'POST Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            #send email or save in database
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html', {'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'blog/contact.html', {'form':form, 'name': name, 'email':email, 'message': message})
    return render(request,'blog/contact.html')


def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."  # Replace with your desired default string
    else:
        about_content = about_content.content
        
    return render(request,'blog/about.html',{'about_content':about_content})