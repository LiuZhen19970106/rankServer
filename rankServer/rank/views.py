from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rank.models import Score, Rank

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
        # 排名表数据更新
        Rank.objects.all().delete()
        score_li = [score_obj.id for score_obj in Score.objects.all().order_by('-score')]
        n = 1
        for i in score_li:
            Rank.objects.create(c_id_id=i, rank=n)
            n = n + 1
        return HttpResponse('upload success')
    elif not client_name:
        return HttpResponse('client_name is required')
    elif not score:
        return HttpResponse('score is required')


def search(request):
    client_name = request.GET.get('client_name', '')
    try:
        start = int(request.GET.get('start', ''))
        end = int(request.GET.get('end', ''))
    except:
        return HttpResponse('start and end must be integer')
    if client_name and start and end:

        if start<1 or start>end or end>1000000:
            return HttpResponse('start and end must be between 1 and 1000000')
        if not Score.objects.filter(client=client_name).first():
            return HttpResponse('client_name has no score in database')
        uscore = Score.objects.filter(client=client_name).first()
        userInfo = {'ranking': uscore.rank.rank, 'client_name': client_name, 'score': uscore.score}
        # rank_list = [rank_obj for rank_obj in Rank.objects.all().order_by('rank')]
        context = {'scores': [{'ranking': scor.rank.rank, 'client': scor.client, 'score': scor.score} for scor in
                              Score.objects.all().order_by('-score')[start - 1:end]], 'userInfo': userInfo}
        if len(context['scores'])<start:
            return HttpResponse('there is no rank in database')
        else:
            return render(request, 'result.html', {'context': context})
    elif not client_name:
        return HttpResponse('client_name is required')
    elif not start or not end:
        return HttpResponse('start and end are required')

    
  