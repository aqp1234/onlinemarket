from django import forms

class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=100, label="제목")
    question = forms.CharField(max_length=1000, label="내용")
    is_secret = forms.BooleanField(label="비밀글", required=False)
