# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
form django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

@csrf_exempt
def ajax_view(request):
    

    return HttpResponse(simplejson.dumps(response))
