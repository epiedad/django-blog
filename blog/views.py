from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

# Create your views here.
def post_list(request, tag_slug=None):
    """Return the list of post in descending order"""

    object_list = Post.published.all()
    tag = None 

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) #3 post per page
    page = request.GET.get('page')


    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        """If page is not an integer, show the first page"""
        posts = paginator.page(1)
    except EmptyPage:
        """If page is out of range, show last page"""
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/post/list.html', { 'posts': posts,
                                                    'page': page,
                                                    'tag': tag })


def post_detail(request, year, month, day, slug):
    """Return a single post"""
    post = get_object_or_404(Post,
                                publish__year=year,
                                publish__month=month,
                                publish__day=day,
                                slug=slug
                            )
    comments = post.comments.filter(active=True) #Return all the comments
    
    if request.method == 'POST':
        #A comment was posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)

            # Assign the current post to the comment
            new_comment.post = post

            # Save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()

    
    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                            .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                            .order_by('-same_tags', '-publish')[:4]
    tags = post.tags.all()

    return render(request, 
                    'blog/post/detail.html', 
                    {'post': post, 
                     'comments': comments,
                     'comment_form': comment_form,
                     'similar_posts': similar_posts,
                     'tags': tags })

def post_share(request, post_id):
    """Retrive post by id"""
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd = None

    if request.method == 'POST':
        """If form was submitted"""
        form = EmailPostForm(request.POST)

        if form.is_valid():
            """Form fields passed validation"""
            cd  = form.cleaned_data
            #send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.\
                format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.\
                format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'cd': cd })

#Search form
def post_search(request):
    form = SearchForm()
    cd = None
    results = None
    total_results = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
                    .filter(content=cd['query']).load_all()
            
            #count total results
            total_results = results.count()

    return render(request, 'blog/post/search.html', {'form': form,
                                                     'cd': cd,
                                                     'results': results,
                                                     'total_results': total_results })
