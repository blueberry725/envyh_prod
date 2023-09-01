from django.shortcuts import render, get_object_or_404
from .models import Post, SliderFeaturedPost, FeaturedPost, Category
from django.core.paginator import Paginator

def home(request):
    # Retrieve active posts, ordered by publication date (descending)
    active_posts = Post.objects.filter(is_active=True).order_by('-pub_date')

    # Paginate the active posts
    paginator = Paginator(active_posts, per_page=7)  # Adjust the per_page as needed
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    # Retrieve slider featured posts and featured posts
    slider_featured_posts = SliderFeaturedPost.objects.filter(post__is_active=True).order_by('order')
    featured_posts = FeaturedPost.objects.filter(is_active=True).order_by('order')

    # Prepare the context to pass to the template
    context = {
        'page_posts': page_posts,
        'sliderFeaturedPosts': slider_featured_posts,
        'featuredPosts': featured_posts
    }

    # Render the home template with the provided context
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    # Retrieve a single post based on the provided slug
    post = get_object_or_404(Post, slug=slug, is_active=True)

    # Prepare the context to pass to the template
    context = {'post': post}

    # Render the post detail template with the provided context
    return render(request, 'blog/article_detail.html', context)

def category_view(request, category_slug):
    # Retrieve the selected category based on the provided category_slug
    category = Category.objects.get(slug=category_slug)

    # Retrieve posts associated with the selected category
    posts = Post.objects.filter(category=category)

    # Set the number of posts per page
    posts_per_page = 10  # Change this as needed

    # Paginate the category posts
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    # Prepare the context to pass to the template
    context = {'category': category, 'page_posts': page_posts}

    # Render the category template with the provided context
    return render(request, 'blog/category.html', context)
