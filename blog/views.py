from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form}) 
  
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post) # request files umožňuje add picures aj 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form}) 
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)
@login_required
def post_remove(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
@login_required
def comment_approve(request, pk): 
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def success_view(request):
    return render(request, 'blog/success.html')

def unsuccess_view(request):
    return render(request, 'blog/unsuccess.html')

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            adresa = 'ruzbacky@yahoo.com'
            predmet = 'Nová zpráva z blog formulára!'
            meno = 'Meno odosielateľa: ' + form.cleaned_data['sender_name']
            sprava = '\nSpráva: ' + form.cleaned_data['message'] 
            hlavicka = '\nJeho emailová adresa:\n' + form.cleaned_data['sender_email']
            hlavicka += "\nMIME-Version: 1.0\nContent-Type: text/html; charset=\"utf-8\"\n"
            predmet_odosielatela = 'Predmet: ' + form.cleaned_data['subject']
            #hlavicka = format_html(
                #"<p>{}</p><p>MIME-Version: 1.0</p><p>Content-Type: text/html; charset=\"utf-8\"</p>",
                #meno + "<br>" + predmet_odosielatela + "<br>" + sprava
            #)    
            uspech = send_mail (predmet, 
                               form.cleaned_data['subject'], 
                               form.cleaned_data['sender_email'], 
                               [adresa], 
                               fail_silently=False, 
                               html_message=meno + hlavicka + predmet_odosielatela + sprava
                               )
            if uspech:
                return redirect('success_view')
        else:
            return redirect('unsuccess_view') 
    else:
        form = EmailForm()    
    return render(request, 'registration/send_email.html', {'form': form})               

# Create your views here.

