from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})

@login_required(login_url='/accounts/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인한 사용자를 작성자로 설정
            post.save()
            return redirect('post_list')  # 게시글 목록 페이지로 리디렉션
    else:
        form = PostForm()
    return render(request, 'board/post_create.html', {'form': form})
