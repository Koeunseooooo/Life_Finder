from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView

from .models import Photo

from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import CrudUser

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'


class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']

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
            return self.render_to_response({'form': form})




class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
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
            return self.render_to_response({'form': form})


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/photo/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user.user_profile:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return redirect('photo:index')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'


from django.views.generic.base import View
from django.http import HttpResponseForbidden, request
from urllib.parse import urlparse

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:    #로그인확인
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user.user_profile
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class PhotoLikeList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:  # 로그인확인
        #     messages.warning(request, '로그인을 먼저하세요')
        #     return HttpResponseRedirect('/')
        return super(PhotoLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여줌
        user = self.request.user.user_profile
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


#######################################################################


from .models import CrudUser
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse


class CrudView(TemplateView):
    template_name = 'photo/photo_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CrudUser.objects.all()
        return context


class CreateCrudUser(View):
    def  get(self, request):
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.create(
            name = name1,
            address = address1,
            age = age1
        )

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)

class DeleteCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateCrudUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)
        address1 = request.GET.get('address', None)
        age1 = request.GET.get('age', None)

        obj = CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.address = address1
        obj.age = age1
        obj.save()

        user = {'id':obj.id,'name':obj.name,'address':obj.address,'age':obj.age}

        data = {
            'user': user
        }
        return JsonResponse(data)