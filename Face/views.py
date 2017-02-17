from django.shortcuts import render
from Avatar import settings
from django.http import HttpResponse
from django.http import JsonResponse
import os
import uuid
from django.views.decorators.csrf import csrf_exempt
import base64 
from tools_face_analyze import analyze_user
import time

# Create your views here.
def index(request):
    return render(request, 'face_index.html', {})

@csrf_exempt
def ajax_uploadimg(request):
    ret = {};
    file = request.POST['img']
    if file:
        path=os.path.join(settings.STATIC_ROOT,'upload') 
        id_img = str(time.time())
        file_name = id_img +".png"        
        path_file = os.path.join(path,file_name)  
          
        imgdata = base64.b64decode(file)  
        f = open(path_file,'wb')
        f.write(imgdata) 
        f.close()

        ret = analyze_user(path_file, id_img)
    else:
        print 'error'

    return JsonResponse(ret)