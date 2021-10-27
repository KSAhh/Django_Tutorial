# 출력
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render # loader와 HttpResponse를 import 하지 않아도 됨

# 에러
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    #### render 이용한 템플릿 내용 출력
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

    #### loader 이용한 템플릿 내용 출력
    # template = loader.get_template('polls/index.html') # polls/index.html 템플릿을 불러옴
    # context = { 
    #     'latest_question_list' : latest_question_list,  # context 전달 (template에 쓰이는 변수명과 python 객체를 연결하는 사전형 값)
    # }
    # return HttpResponse(template.render(context, request))
    
    #### HttpResponse 이용한 템플릿 내용 출력
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

def detail(request, question_id):
    #### get_object_or_404를 이용한 error
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

    #### Http404를 이용한 error
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'qeustion':question})

    #### HttpResponse 이용한 간단한 출력
    # return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)