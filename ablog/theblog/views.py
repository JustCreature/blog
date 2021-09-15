from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from .forms import PostForm, EditForm
from django.http import HttpResponseRedirect

# Create your views here.

# def home(request):
#     return render(request, 'theblog/home.html', {})
from .models import Post, Category


class HomeView(ListView):
    model = Post
    template_name = 'theblog/home.html'
    ordering = ['-post_date']

    def get_context_data(self, *args, object_list=None, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'theblog/article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['cat_menu'] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'theblog/add_post.html'
    # fields = '__all__'

class AddCategoryView(CreateView):
    model = Category
    # form_class = PostForm
    template_name = 'theblog/add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'theblog/update_post.html'
    # fields = ('title', 'title_tag', 'body')

class DeletePostView(DeleteView):
    model = Post
    template_name = 'theblog/delete_post.html'
    success_url = reverse_lazy('home')

def CategoryListView(request):
    cat_menu_list = Category.objects.all()

    context = {
        'cat_menu_list': cat_menu_list,
    }

    return render(request, 'theblog/category_list.html', context)

def CategoryView(request, cats):

    category_posts = Post.objects.filter(category=cats)

    context = {
        'cats': cats,
        'category_posts': category_posts,
    }

    return render(request, 'theblog/categories.html', context)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))