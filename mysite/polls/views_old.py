from django.shortcuts import render

# Create your views here.

#from django.http import HttpResponse
#from django.template import loader
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Choice, Question

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #return HttpResponse("Voce esta olhando as perguntas %s." %question_id)
    """try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Questao nao existe")
    return render(request, 'polls/detail.html',{'question': question})"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "Voce esta olhando para os resultados das perguntas %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    #return HttpResponse("Voce esta votando na questao %s." %question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=   request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "vc nao escolheu uma saida"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))