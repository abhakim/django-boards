from django.shortcuts import (render, HttpResponse, 
                            get_object_or_404, redirect)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db.models import Count
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView
from django.views.generic import ListView

from boards.models import Board, Post, Topic
from boards.forms import NewTopicForm, PostForm


# Create your views here.
# def board_list(request):
#     boards = Board.objects.all()
#     return render(request, 'home.html', {'boards':boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/board_list.html'

# def topic_list(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
#     page = request.GET.get('page', 1)

#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # fallback to the first page
#         topics = paginator.page(1)
#     except EmptyPage:
#         # probably the user tried to add a page number
#         # in the url, so we fallback to the last page
#         topics = paginator.page(paginator.num_pages)

#     return render(request, 'topics.html', {'board': board, 'topics': topics})

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topic_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)

#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         user = User.objects.first()
#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )

#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )

#         return redirect('board_topics', pk=board.pk)
#     return render(request, 'new_topic.html', {'board': board})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('post_list', pk=board.pk, topic_pk=topic.board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'boards/new_topic.html', {'board': board, 'form': form})

# def post_list(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'boards/post_edit.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('post_list', pk=post.topic.board.pk, topic_pk=post.topic.pk)
    
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('post_list', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'boards/reply_topic.html', {'topic': topic, 'form': form})

