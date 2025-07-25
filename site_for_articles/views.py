from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import comment
from django.core.mail import send_mail
from .forms import CommentForm,EmailPostForm
from .models import  Post
from  django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day,slug):
    post= get_object_or_404(Post,slug=slug,status='published', publish__year=year, publish__month=month, publish__day=day)


    comments=post.comments.filter(active=True)
    print(comments)
    new_comment=None

    if request.method=='POST':
        comment_form= CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()

    else:
        comment_form=CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post':post,
                   'comments':comments,
                   "new_comment":new_comment,
                   "comment_form":comment_form
                   })


def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status="published")
    sent=False

    if request.method=='POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            print(cd)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            title=f"{cd['name']} sizga {post.title} ni o'qishni taklif etadi."
            message=f'Read {post.title} at {post_url}\n\n'\
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(title,message, 'munisabax2002@gmail.com', [cd['to']], fail_silently=False)
            sent=True


    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                                            'form':form,
                                                                            'sent': sent})
