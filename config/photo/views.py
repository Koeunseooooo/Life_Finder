from django.shortcuts import render, redirect,reverse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Photo
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
# from .forms import PhotoForm
from create_profile.models import Profile
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from django.contrib import messages

import datetime
from photo.forms import PhotoForm


class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

    # pagination
    paginate_by = 10  # Display 10 objects per page

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context



from django_summernote.widgets import SummernoteWidget
class PhotoCreate(CreateView):
    model = Photo
    form_class = PhotoForm

    # fields = ['author','text', 'image']
    # fields = ['text', 'image']
    template_name_suffix = '_create'
    # success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user.user_profile
        if form.is_valid():
            # 올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('photo:index')

        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form,})



class PhotoUpdate(UpdateView):
    model = Photo

    form_class = PhotoForm

    # fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user.user_profile:
            messages.warning(request, '수정할 권한이 없습니다.')
            return redirect('photo:detail')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/photo/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user.user_profile:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return redirect('photo:detail')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

from .forms import CommentForm
class PhotoDetail(DetailView, FormMixin):
    model = Photo
    template_name_suffix = '_detail'
    form_class =CommentForm
    def get_success_url(self,**kwargs):
        return reverse('photo:detail',kwargs={'pk':self.object.pk})
    def get_context_data(self, **kwargs):
        context = super(PhotoDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={
            'text': '댓글을 입력해주세요.',
        })
        context['user'] = self.request.user
        context['comments'] = self.object.photo_comment
        return context
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        comment = form.save(commit = False)
        comment.photo = get_object_or_404(Photo,pk=self.object.pk)
        comment.comment_author = self.request.user.user_profile
        comment.save()
        return super(PhotoDetail,self).form_valid(form)


from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse


class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/like_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PhotoMyList(ListView):
    model = Photo
    template_name = 'photo/photo_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(PhotoMyList, self).dispatch(request, *args, **kwargs)


