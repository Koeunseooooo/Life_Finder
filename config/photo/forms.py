from django import forms
from .models import Photo, Comment
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.forms import TextInput
from django_summernote.widgets import SummernoteWidget
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title','text', 'image']
        widgets = {
            'text': SummernoteWidget(),
            'title': TextInput(attrs={'placeholder': ' 제목을 작성해주세요.'}),
        }


        # def __init__(self, *args, **kwargs):
        #     super(PhotoForm, self).__init__(*args, **kwargs)
        #
        #     for fieldname in ['title', 'text']:
        #         self.fields[fieldname].help_text = None
        #         self.fields['title'].widget.attrs.update({'placeholder': '    제목을 작성해주세요'})
        #         self.fields['title'].label = ''
        #         self.fields['text'].widget.attrs.update({'placeholder': '    본문을을 작성해주세요'})
        #         self.fields['text'].label = ''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': TextInput(attrs={'placeholder': '댓글을 입력해주세요.'}),
        }

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.fields['text'].label = '댓글'