from django.shortcuts import redirect

def home(request):
    # Redireciona para a lista de eventos
    return redirect('events:event_list')
