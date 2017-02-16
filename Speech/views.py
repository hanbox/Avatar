# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import time

from .models import Speech_main

# import jieba
from collections import Counter
# jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数

from snownlp import SnowNLP

User = get_user_model()

# Create your views here.
def index(request):
    return render(request, 'iat.html', {})

def ajax_analyze(request):
    speech_data = request.GET.get('speech_data')
    s = SnowNLP(speech_data)
    #seg_list = jieba.cut(speech_data)  # 默认是精确模式
    count_dict = dict(Counter(s.words))
    analyze_dict = {}
    analyze_dict['count_dict'] = count_dict;
    analyze_dict['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()));
    analyze_dict['sentiments'] = s.sentiments
    analyze_dict['keywords'] = s.keywords(3)

    Speech_main.objects.create(data=speech_data, sentiments=s.sentiments)

    return JsonResponse(analyze_dict)