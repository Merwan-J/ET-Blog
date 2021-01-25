from django import forms
from .models import Comment,Author, Post
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE): 
    def use_required_attribute(self, *args): 
        return False

class PostForm(forms.ModelForm):
    body = forms.CharField( 
        widget=TinyMCEWidget( 
            attrs={'required': False, 'cols': 30, 'rows': 10,'class': 'form-control'} 
        ) 
    ) 
    title = forms.CharField( 
        widget=forms.TextInput( 
            attrs={'class': 'form-control'} 
        ) 
    ) 

    
    
    class Meta:
        model = Post
        fields = ('title','body','thumbnail','catagory','previous_post', 'next_post',)


class CommentForm(forms.ModelForm):
    body = forms.CharField( 
        widget=forms.Textarea( 
            attrs={'class': 'form-control', 'name':"usercomment" ,'id':"usercomment" ,'placeholder':"Type your comment"} 
        ) 
    ) 
    
    class Meta:
        model = Comment
        fields = ('body',)
        