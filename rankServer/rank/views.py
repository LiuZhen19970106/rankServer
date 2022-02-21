from django.http import JsonResponse
from django.db.models.functions import Rank
from django.db.models import Window, F
from django.shortcuts import render
from rank.models import Score

class ErrorMessage():
    UPLOAD_SCORE_ERROR = 'score must be number and between 1 and 10000000'
    UPLOAD_CLENT_ERROR = 'client_name is required'
    UPLOAD_MISS_SCORE_ERROR = 'score is required'
    SEARCH_FILLTER_ERROR = 'start and end must be number '
    SEARCH_CLIENT_ERROR = 'client_name is required'
    SEARCH_INVALID_START_END = 'start must greater than or equal to 1 or start must be less than end'
    SEARCH_MISS_CLIENT_ERROR = 'client_name is not exist'
    SEARCH_SCORE_ERROR = 'there is no data in database'

def generate_res(status_code, message, data):
    return {
        'status_code': status_code,
        'msg': message,
        'data': data
    }

# Create your views here.
def upload(request):
    
    client_name = request.GET.get('client_name', '')
    try:
        score = float(request.GET.get('score', ''))
    except:
        
        return JsonResponse(generate_res(400, 'failed', ErrorMessage.UPLOAD_SCORE_ERROR))
    if client_name and score:
        if score<1 or score>10000000:
            return JsonResponse(generate_res(400, 'failed', ErrorMessage.UPLOAD_SCORE_ERROR))
        old_scor = Score.objects.filter(client=client_name).first()
        if old_scor:
            if old_scor.score != score:
                old_scor.score = score
                old_scor.save()
        else:
            Score.objects.create(client=client_name, score=score)
        return JsonResponse(generate_res(200, 'success', 'upload success'))
    elif not client_name:
        return JsonResponse(generate_res(400, 'failed', ErrorMessage.UPLOAD_CLENT_ERROR))
    elif not score:
        return JsonResponse(generate_res(400, 'failed', ErrorMessage.UPLOAD_MISS_SCORE_ERROR))


def search(request):
    client_name = request.GET.get('client_name', '')
    start = request.GET.get('start', 1)
    end = request.GET.get('end', Score.objects.all().count())
    
    try:
        start = int(start)
        end = int(end)
        if end>Score.objects.all().count():
            end = Score.objects.all().count()
    except:
        return JsonResponse(generate_res(400, 'failed', ErrorMessage.SEARCH_FILLTER_ERROR))
        
    if client_name:
        if start<1 or start>end:
            return JsonResponse(generate_res(400, 'failed', ErrorMessage.SEARCH_INVALID_START_END))
            
        if not Score.objects.filter(client=client_name).first():
            return JsonResponse(generate_res(400, 'failed', ErrorMessage.SEARCH_MISS_CLIENT_ERROR))
            
        # 获取排名
        get_rank = Score.objects.all().annotate(score_rank=Window(expression=Rank(), order_by=F('score').desc())).values('score_rank', 'client', 'score')
        user_rank = list(filter(lambda x: x['client'] == client_name, get_rank))[0]
        userInfo = {'ranking': user_rank['score_rank'], 'client_name': client_name, 'score': user_rank['score']}
        context = {'scores': [{'ranking': scor['score_rank'], 'client': scor['client'], 'score': scor['score']} for scor in
                              get_rank[start - 1:end]], 'userInfo': userInfo}

        if len(context['scores'])<start:
            return JsonResponse(generate_res(400, 'failed', ErrorMessage.SEARCH_SCORE_ERROR)) 
        else:
            return render(request, 'result.html', {'context': context})
    elif not client_name:
        return JsonResponse(generate_res(400, 'failed', ErrorMessage.SEARCH_CLIENT_ERROR))
        

