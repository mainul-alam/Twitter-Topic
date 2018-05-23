from django import forms


class TopicForm(forms.Form):
    name = forms.CharField(label='Topic Name', max_length=100)
    description = forms.CharField(label='Topic Name', widget=forms.Textarea, max_length=250)


class CommentForm(forms.Form):
    topic_id = forms.IntegerField(label='', widget=forms.HiddenInput)
    comment = forms.CharField(label='Comment', widget=forms.Textarea, max_length=50)



