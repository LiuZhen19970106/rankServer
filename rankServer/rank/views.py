from django.http import HttpResponse, JsonResponse
from django.db.models.functions import Rank
from django.db.models import Window, F
from django.shortcuts import render
from rank.models import Score

# Create your views here.
def upload(request):
    
    client_name = request.GET.get('client_name', '')
    try:
        score = float(request.GET.get('score', ''))
    except:
        return HttpResponse('score must be number and between 1 and 10000000')
    if client_name and score:
        if score<1 or score>10000000:
            return HttpResponse('score must be between 1 and 10000000')
        old_scor = Score.objects.filter(client=client_name).first()
        if old_scor:
            if old_scor.score != score:
                old_scor.score = score
                old_scor.save()
        else:
            Score.objects.create(client=client_name, score=score)
        return HttpResponse('upload success')
    elif not client_name:
        return HttpResponse('client_name is required')
    elif not score:
        return HttpResponse('score is required')


def search(request):
    client_name = request.GET.get('client_name', '')
    start = request.GET.get('start', 1)
    end = request.GET.get('end', Score.objects.all().count())

    try:
        start = int(start)
        end = int(end)
    except:
        return HttpResponse('start and end must be integer')
    
    if client_name:
        if start<1 or start>end or end>1000000:
            return HttpResponse('start and end must be between 1 and 1000000')
        if not Score.objects.filter(client=client_name).first():
            return HttpResponse('client_name has no score in database')
        # 获取排名
        get_rank = Score.objects.all().annotate(score_rank=Window(expression=Rank(), order_by=F('score').desc())).values('score_rank', 'client', 'score')
        user_rank = list(filter(lambda x: x['client'] == client_name, get_rank))[0]
        userInfo = {'ranking': user_rank['score_rank'], 'client_name': client_name, 'score': user_rank['score']}
        context = {'scores': [{'ranking': scor['score_rank'], 'client': scor['client'], 'score': scor['score']} for scor in
                              get_rank[start - 1:end]], 'userInfo': userInfo}

        if len(context['scores'])<start:
            return HttpResponse('there is no rank in database')
        else:
            return render(request, 'result.html', {'context': context})
    elif not client_name:
        return HttpResponse('client_name is required')

