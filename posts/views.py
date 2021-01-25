from django.shortcuts import render,HttpResponseRedirect,redirect,reverse,get_object_or_404,HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import Post,Comment,Catagory,Author
from subscribers.models import Subscriber
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.





def get_author(user):
    qs = Author.objects.filter(author=user)
    if qs.exists():
        return qs[0]
    return None

def search_view(request):
    query = request.GET.get('search')
    queryset = Post.objects.all().filter(Q(title__icontains=query) | Q(body__icontains=query)).distinct()
    if queryset:
        paginator = Paginator(queryset,4)
        page_num = request.GET.get('page')
        queryset = paginator.get_page(page_num)
        
    return render(request,'search.html',context={'query_set':queryset,'query':query})


def index(request):
    latest_posts = Post.objects.order_by('-date_created')[:3]
    all_post = Post.objects.all()[:3]
    #########################
    # I wanna get the Catagory of the post but cant do it
    ########################
    context = {'latest_posts':latest_posts,'all_post':all_post}
    if request.method =='POST':
        email = request.POST['email']
        try:
            sub = Subscriber.objects.get(email=email)
        except :
            Subscriber.objects.create(email=email)
        
    return render(request,'index.html',context=context)


def blog_view(request):
    catagories = Catagory.objects.all()
    latest_posts = Post.objects.order_by('-date_created')[:3]
    all_post = Post.objects.all()
    paginator = Paginator(all_post,4)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    print(catagories)
    context = {'latest_posts':latest_posts,'page_obj':page_obj,'catagories':catagories}
    return render(request,'blog.html',context=context)


def post_detail(request, pk):
    post_obj = Post.objects.get(pk=pk)
    latest_posts = Post.objects.order_by('-date_created')[:3]
    commnent_set = post_obj.comments.all()
    catagories = Catagory.objects.all()
    comment_form = CommentForm()
    context = {'latest_posts':latest_posts,'post':post_obj,'catagories':catagories,'comments':commnent_set,'comment_form':comment_form}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(post_obj)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    count_hit=True
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    if request.method=='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.author = request.user
            comment_form.instance.Post = post_obj
            comment_form.save()
            return redirect(post_obj)
        else:
            return redirect(post_obj)
    print(request.path)
    return render(request,'post_detail.html',context=context)

@login_required(login_url='/accounts/login')
def create_post(request):
    form = PostForm()
    context={}
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)
        author = get_author(request.user)
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post_detail',kwargs={'pk':form.instance.pk}))
        else:
            print(form)
            print(request.POST)
            print("form not valid #############")
            return redirect(reverse('create'))
    else:
        context={'form':form}
    return render(request,'create_post.html',context=context)

@login_required(login_url='/accounts/login')
def post_delete(request,pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.author.author:
        post.delete()
        return redirect(reverse('blog'))
    return HttpResponse("Permission denied!")


@login_required(login_url='/accounts/login')
def update_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    form = PostForm(request.POST or None,request.FILES or None,instance=post)
    if request.user == post.author.author:
        if request.method =='POST':
            author = get_author(request.user)
            if form.is_valid():
                form.instance.author=author
                form.save()
                return redirect(reverse('post_detail',kwargs={'pk':pk}))
            else:
                print("#######form not valid")
                return redirect(reverse('update_post',kwargs={'pk':pk}))
        else:
            context={'form':form}
            return render(request,'update_post.html',context=context)
        
    return HttpResponse("Permission denied!")
def catagory_view(request,catagory):
    query = catagory
    print(query)
    catagory = Catagory.objects.get(name=query)
    queryset = catagory.posts.all()
    if query:
        paginator = Paginator(queryset,4)
        page_num = request.GET.get('page')
        queryset = paginator.get_page(page_num)
        
    return render(request,'search.html',context={'query_set':queryset,'query':query,'cata_search':True})

