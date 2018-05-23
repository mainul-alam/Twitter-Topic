from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from .forms import TopicForm, CommentForm
from .models import Topic, Comment, User,TwitterApi, Subscriber
from allauth.socialaccount.models import SocialAccount, SocialToken
import twitter





# Create your views here.


class HomePage(TemplateView):

    def get(self, request, **kwargs):
        subscriptions = Subscriber.objects.filter(user=request.user)

        tweets = TwitterApi.getTweetsByUser(request.user)
        return render(request, 'home.html', {'tweets': tweets, 'subscriptions': subscriptions})


# TOPIC CREATING VIEW #
class TopicFormView(TemplateView):
    form_class = TopicForm
    initial = {'name': 'New topic ..', 'description': 'description here..'}

    def get(self, request, **kwargs):
        form = self.form_class(initial=self.initial)

        return render(request, 'topics/create_new-topic.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            topic = Topic(name=data['name'], description=data['description'], user=request.user)
            topic.save()

            return redirect('/topics')
        else:
            return render(request, 'topics/create_new-topic.html', {'form': form})



# TOPIC YOU HAVE CREATED VIEW #

class TopicView(TemplateView):
    def get(self, request, **kwargs):
        topics = Topic.objects.filter(user_id=request.user.id)
        return render(request, 'topics/all_your_topics.html', {'topics': topics})



# ALL TOPIC VIEW #

class AllTopicView(TemplateView):
    def get(self, request, **kwargs):
        all_topics = Topic.objects.all()
        return render(request, 'topics/all_topics.html', {'all_topics': all_topics})



# TOPIC DESCRIPTION VIEW #

class TopicConversationView(View):
    def get(self, request, **kwargs):
        topic_id = kwargs['topic_id']
        topic = Topic.objects.get(id=topic_id)
        comments = Comment.objects.filter(topic_id=topic.id)

        comment_form = CommentForm(initial={'topic_id': topic.id, 'comment': 'New comment'})
        return render(request, 'topics/show_topic_details.html',
                      {'topic': topic, 'comments': comments, 'comment_form': comment_form})

# COMMENT VIEW #

class CommentView(View):
    def post(self, request, **kwargs):
        form = CommentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            topic = Topic.objects.get(id=data['topic_id'])

            if request.POST.get('tweet_btn'):
                tweet = TwitterApi.postTweet(request.user, data['comment'])
                comment = Comment(user=request.user, topic=topic, tweet_id=tweet.id)
            elif request.POST.get('comment_btn'):
                comment = Comment(comment=data['comment'], user=request.user, topic=topic)

            comment.save()
            return redirect('show_topic', topic.id)
        else:
            return render(request, 'topics/show_topic_details.html', {'comment_form': form})


# FOR DELETING COMMENTS #

def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    topic_id = comment.topic_id

    comment.delete()
    return redirect('show_topic', topic_id)

# FOR DELETING TOPICS #

def delete_topic(request, pk):
    topic = Topic.objects.get(id=pk)

    topic.delete()
    return redirect('topics')

# FOR SUBSCRIBING TOPIC #
def subscribe_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    subscription = Subscriber(topic=topic, user=request.user)
    subscription.save()
    return redirect('topics')

def unsubscribe_topic(request, pk):
    subscription = Subscriber.objects.get(id=pk)
    subscription.delete()
    return redirect('home')
