import facebook
from django.shortcuts import render, redirect
from .models import Post
import csv
from django.http import HttpResponse

# Facebook API credentials
ACCESS_TOKEN = 'your_facebook_access_token'

def fetch_posts(url):
    graph = facebook.GraphAPI(access_token=ACCESS_TOKEN)
    post_data = graph.get_object(url + '/posts?fields=id,message,likes.summary(true),shares,comments.summary(true),created_time')
    return post_data['data']

def home(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        posts = fetch_posts(url)
        
        # Save posts in database (if needed)
        for post in posts:
            Post.objects.create(
                post_id=post['id'],
                content=post.get('message', ''),
                likes=post['likes']['summary']['total_count'],
                shares=post.get('shares', {}).get('count', 0),
                comments=post['comments']['summary']['total_count'],
                post_date=post['created_time']
            )
        return redirect('display_posts')
    return render(request, 'home.html')

def display_posts(request):
    posts = Post.objects.all()
    return render(request, 'display_posts.html', {'posts': posts})

def export_csv(request):
    # Get selected posts
    post_ids = request.POST.getlist('post_ids')
    posts = Post.objects.filter(post_id__in=post_ids)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="selected_posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['Post ID', 'Content', 'Likes', 'Shares', 'Comments', 'Post Date'])
    for post in posts:
        writer.writerow([post.post_id, post.content, post.likes, post.shares, post.comments, post.post_date])

    return response
