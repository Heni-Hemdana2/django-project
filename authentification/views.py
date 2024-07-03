from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from supervisor.models.supervisor import Supervisor
from .forms import SupervisorLoginForm , ClientLoginForm
from django.contrib.auth.hashers import check_password
from client.models                  import Client


# Définition de la vue pour la connexion des superviseurs
def supervisor_login(request):
    # Vérification si la méthode de requête est POST
    if request.method == 'POST':
    # Instanciation du formulaire avec les données POST

        form = SupervisorLoginForm(request.POST)
        # Vérification si le formulaire est valide

        if form.is_valid():
            
            email = form.cleaned_data['email']# Récupération de l'email depuis les données nettoyées du formulaire
            
            supervisor = Supervisor.objects.get(email=email)# Récupération de l'objet Supervisor correspondant à l'email
            
            login(request, supervisor.user)  # Connexion de l'utilisateur associé au superviseur
            # Mise à jour de la session pour indiquer que le superviseur est authentifié
            request.session['supervisor_authenticated'] = True
            #request.session['client_authenticated'] = False
            next_url = request.POST.get('next', 'dashboard_super')
            return redirect(next_url)
        return render(request, 'pages/supervisor.html', {'form': form})
    form = SupervisorLoginForm()
    return render(request, 'pages/supervisor.html', {'form': form})


def sign_out(request):
    if request.session.get('supervisor_authenticated'):
        request.session.flush()
        logout(request)
    return redirect('supervisor_login')



def client_login(request):
    if request.method == 'POST':
        form_client = ClientLoginForm(request.POST)
        if form_client.is_valid():
            email = form_client.cleaned_data['email']
            password = form_client.cleaned_data['password']
            try:
                client = Client.objects.get(email=email)
                if check_password(password, client.password):
                    login(request, client.user)
                    request.session['client_authenticated'] = True
                    request.session['supervisor_authenticated'] = False
                    next_url = request.POST.get('next', 'select_project_of_project')
                    return redirect(next_url)
                else:
                    form_client.add_error(None, "Invalid email or password!!!")
            except Client.DoesNotExist:
                form_client.add_error(None, "Invalid email or password!!!")
        return render(request, 'pages/client.html', {'form_client': form_client})
    form_client = ClientLoginForm()
    return render(request, 'pages/client.html', {'form_client': form_client})


def sign_out_client(request):
    if request.session.get('client_authenticated'):
        request.session.flush()
        logout(request)
    return redirect('client_login')




