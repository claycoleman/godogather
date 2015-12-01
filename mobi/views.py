from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse
from main.models import Event, Group, Profile

def event_detail_view(request, pk):  
    event = Event.objects.get(pk=pk)

    context = {}
    context['event'] = event

    return render_to_response('event_detail.html', context, context_instance=RequestContext(request))


def event_list_view(request):

    events = Event.objects.all()

    context = {}
    context['events'] = events

    return render_to_response('event_list.html', context, context_instance=RequestContext(request))


