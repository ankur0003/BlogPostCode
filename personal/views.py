from django.shortcuts import render
from blog.models import BlogPost
from blog.views import get_blog_queryset
from operator import attrgetter
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
# Create your views here.
#def home_screen_view(request):
# 	context = {}
# 	context['some_string'] = "This is some string"
# 	list_of_things = []
# 	list_of_things.append("First Entry")
# 	list_of_things.append("Second Entry")
# 	list_of_things.append("Third Entry")
# 	context['list_val']=list_of_things

# 	return render(request,"personal/home.html",context)
BLOG_POSTS_PER_PAGE = 10
def home_screen_view(request):
	context={}
	query=""
	if request.GET:
		query=request.GET.get('q','')
		context['query']=str(query)
	#Below is a selectg all query
	blog_posts = sorted(get_blog_queryset(query),key=attrgetter('date_updated'), reverse=True)
	#context['blog_posts']=blog_posts
	page = request.GET.get('page',1)
	blog_post_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
	try:
		blog_posts = blog_post_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_post_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_post_paginator.page(blog_post_paginator.num_pages)
	
	context['blog_posts'] = blog_posts

	return render(request,"personal/home.html",context)
