
from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('name', 'email', 'body')
        # labels={'name':"Ismingiz",
        #         'email':"email manzilingiz",
        #         'body':"izohingiz",
        #         }
class EmailPostForm(forms.Form):
    name=forms.CharField(max_length=25)
    email=forms.EmailField()
    to= forms.EmailField()
    comments=forms.CharField(required=False,
                             widget=forms.Textarea)