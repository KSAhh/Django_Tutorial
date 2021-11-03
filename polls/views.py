# 출력
from django.http import HttpResponse, HttpResponseRedirect # 출력
from django.template import loader # 출력
from django.shortcuts import render # loader와 HttpResponse를 import 하지 않아도 됨
from django.urls import reverse # vote 기능에 사용하는 redering
from django.views import generic # generic view
from django.utils import timezone

# 에러
from django.http import Http404 # 오류 생성
from django.shortcuts import get_object_or_404 # 오류 생성

from .models import Question, Choice


#### generic view
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    #### 오류 수정 후
    def get_queryset(self):
        """Return the last published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    #### 오류 수정 전
    # def get_queryset(self):
    #     """Return the last five published question."""
    #     return Question.objects.order_by('-pub_date')[:5]

#### 어려운 view
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]

#     #### render 이용한 템플릿 내용 출력
#     context = {'latest_question_list' : latest_question_list}
#     return render(request, 'polls/index.html', context)

#     #### loader 이용한 템플릿 내용 출력
#     # template = loader.get_template('polls/index.html') # polls/index.html 템플릿을 불러옴
#     # context = { 
#     #     'latest_question_list' : latest_question_list,  # context 전달 (template에 쓰이는 변수명과 python 객체를 연결하는 사전형 값)
#     # }
#     # return HttpResponse(template.render(context, request))
    
#     #### HttpResponse 이용한 템플릿 내용 출력
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#-------------------------------------------------------------------------------------------------------

#### generic view
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    #### 오류 수정 전
    #### 오류 수정 후 (추가)
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

#### 어려운 view
# def detail(request, question_id):
#     #### get_object_or_404를 이용한 error
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})

#     #### Http404를 이용한 error
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'qeustion':question})

#     #### HttpResponse 이용한 간단한 출력
#     # return HttpResponse("You're looking at question %s." % question_id)
#-------------------------------------------------------------------------------------------------------

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
#-------------------------------------------------------------------------------------------------------

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # 선택된 설문의 id를 문자열로 반환
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message':"You didn't select a choicce.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#    return HttpResponse("You're voting on question %s." % question_id)
#-------------------------------------------------------------------------------------------------------
#### generic view
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#### 어려운 view
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':question})