from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template import loader

from seleniumtest.models import Question


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'seleniumtest/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)


def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('seleniumtest/index.html')
    context = {'latest_questions': latest_questions}
    return HttpResponse(template.render(context, request))


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
