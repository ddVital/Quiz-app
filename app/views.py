from pickle import FALSE
from unittest import result
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, ListView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout

from .models import Answer, Notification, Question, Quiz, Result, User
from .forms import Login_form, Register_form, SettingsForm


# Create your views here.
def index(request):
    context = {"quizes": Quiz.objects.all()[:4]}

    return render(request, "core/index.html", context)


class QuizView(DetailView):
    ''' QUIZ view'''
    model = Quiz
    context_object_name = "quiz"
    template_name = 'core/quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = Quiz.objects.get(id=self.object.id)
        context = {"quiz": quiz}
        
        return context


def quiz_data_view(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({"question": str(q), "answer": answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


# class QuizResults()
# def quiz_results(request, slug):
#     quiz = Quiz.objects.get(slug=slug)
#     score = 0

#     if request.method == "POST":
#         for question in quiz.get_questions():
#             user_answer = request.POST.get(f'{question.pk}-answer')
#             correct_answer = question.get_answers().get(correct=True).text
#             if check_answer(user_answer, correct_answer):
#                 score += 1
#             # print(f"\n {question.get_answers().get(correct=True).text}: ")
#             # print(f"{question.get_answers().get(correct=True).text == user_answer}")
#             # print(f"{user_answer} \n\n\n")

#         print(score)
#         calc_score(score, quiz.get_questions().count())
#         save_user_marks(request.user, quiz, score)

#     return render(request, "core/results.html")


# class ResultsView(DetailView):
#     model = Result
#     context_object_name = "results"
#     template_name = "core/results.html"

#     def get_context_data(self, **kwargs):
#         # context = super().get_context_data(**kwargs)
#         quiz = Quiz.objects.get(slug=self.object.slug)
#         result = Result.objects.get(quiz=quiz)
#         context = {"results": result}
        
#         return context

def quiz_results(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    result = Result.objects.get(quiz=quiz, user=request.user)
    context = {"results": result}
    return render(request, "core/results.html", context)


def check_results(request, slug):
    quiz = Quiz.objects.get(slug=slug)
    score = 0

    if request.method == "POST":
        for question in quiz.get_questions():
            user_answer = request.POST.get(f'{question.pk}-answer')
            correct_answer = question.get_answers().get(correct=True).text
            if check_answer(user_answer, correct_answer):
                score += 1
            # print(f"\n {question.get_answers().get(correct=True).text}: ")
            # print(f"{question.get_answers().get(correct=True).text == user_answer}")
            # print(f"{user_answer} \n\n\n")

        print(score)
        score_in_percents = calc_score(score, quiz.get_questions().count())
        save_user_marks(request.user, quiz, score_in_percents)

    return HttpResponseRedirect(reverse("quiz_results", kwargs={'slug': slug}))


def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        return True
    return False


def calc_score(score, number_of_questions):
    total_score = ((score/number_of_questions)*100)
    return total_score


def save_user_marks(user, quiz, score):
    result = Result.objects.filter(user=user, quiz=quiz)
    if result.exists():
        mark = Result.objects.update(score=score)
    else:
        mark = Result.objects.create(user=user, quiz=quiz, score=score)
        
    print(mark)


def user_profile(request, username):
    ''' User profile '''
    context = {"profile": User.objects.get(username=username)}
    return render(request, "core/profile.html", context)


def follow(request, username):
    ''' username is the user that will be followed '''
    user = request.user
    follow = User.objects.get(username=username)
    user.following.add(follow)
    follow.followers.add(user)
    user.save()
    follow.save()
    create_notification(follow, f"{follow.username} started following you.")

    return HttpResponseRedirect(reverse("index"))


def unfollow(request, username):
    ''' username is the user that will be unfollowed '''
    user = request.user
    follow = User.objects.get(username=username)
    user.following.remove(follow)
    follow.followers.remove(user)
    user.save()
    follow.save()

    return HttpResponseRedirect(reverse("index"))


class SettingsView(UpdateView):
    model = User
    form_class = SettingsForm
    template_name = "core/settings.html"
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("settings"))


def explore(request):
    ''' Explore items '''
    context = {"quizes": Quiz.objects.all()[:4]}
    return render(request, "core/explore.html", context)


def search(request):
    ''' search view '''
    search = request.GET['q']
    difficulty = request.GET['difficulty']
    results = Quiz.objects.filter(name__contains=search)

    context = {
        "results": results,
        "search": search
    }
    return render(request, "core/search.html", context)


def categories(request, category):
    ''' Filter items by category '''
    context = {"results": Quiz.objects.filter(category=category)} # filter category items
    return render(request, 'core/category.html', context)


def personalize(request):
    ''' Change theme, and personalize items '''
    user = request.user
    # context = {user}
    if request.method == "POST":
        theme = request.POST.get("theme")
        user.theme = theme
        user.save()
        
    return render(request, "core/personalize.html")


def update_avatar(request):
    ''' update the profile picture '''
    user = request.user
    if request.method == "POST":
        pic = request.POST.get('pic')
        user.avatar = pic
        user.save()
        
    return HttpResponseRedirect(reverse("settings"))


def create_notification(user, msg):
    ''' Notification parameter is a dict with the user, name, and desc of the notification '''
    new_notification = Notification.objects.create(user=user, name=msg, desc="")
    new_notification.save()


def mark_as_read(user):
    ''' mark notifications as read '''
    notification = Notification.objects.filter(user=user, read=False)
    notification.update(read=True)
    # notification.save()


def delete_notification(request, id):
    ''' ID is the notification id '''
    notification = Notification.objects.get(id=id, user=request.user)
    notification.delete()
    
    return HttpResponseRedirect(reverse('notifications'))



def notifications(request):
    ''' display the user notifications '''
    mark_as_read(request.user)
    return render(request, "core/notifications.html")


def logout_view(request):
    ''' logout the user '''
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    ''' Log in '''
    context = {"form": Login_form()}

    if request.method == "POST":
        form = Login_form(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                create_notification(user, f"A new device was signed in to @{user.username} account at 192.168.1.42.") # TODO: add the actual ip address, TODO: users will get a notification to every user that logs in 
                return HttpResponseRedirect(reverse("index"))
            else:
                context["error"] = "Invalid username and/or password."
                return render(request, "core/login.html", context)

    return render(request, "core/login.html", context)


class Register(CreateView):
    ''' Create a new user '''
    model = User
    form_class = Register_form
    template_name = "core/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse("index"))


def delete_account(request):
    ''' Delete the user account '''
    user = User.objects.get(username=request.user.username)
    user.delete()
    return HttpResponseRedirect(reverse("login"))