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

def send_email(request):
    hlaska = ''
    if request.method == 'POST':
        meno = request.POST.get('meno')
        email = request.POST.get('email')
        sprava = request.POST.get('správa')
        rok = request.POST.get('rok')
    
        if meno and email and sprava and rok == str(datetime.now().year):
            adresa = 'ruzbacky@yahoo.com'
            predmet = 'Nová správa z mailformu'
            sprava_emailu = f'''
                <html>
                    <body>
                        <h2>Nová správa z mailformu</h2>
                        <p>Od: {meno}</p>
                        <p>Email: {email}</p>
                        <p>Správa: {sprava}</p>
                    </body>
                </html>
            '''
    
            try:
                send_mail(predmet, sprava_emailu, email, [adresa], html_message=sprava_emailu)
                hlaska = 'Email bol úspešne odoslaný, čoskoro Vám odpovieme.'
            except:
                hlaska = 'Email sa nepodarili odoslať. Skontrolujte adresu!'
        else:
            hlaska = 'Formulár nie je správne vyplnený!'
            
    return render(request, 'web_formulár.html', {'hlaska': hlaska})
                

# Create your views here.

