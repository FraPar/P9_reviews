from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

# from .models import ALBUMS # commentez cette ligne

# Create your views here.

from . import forms, models

from django.template import loader

@login_required
def ticket_upload(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if any([ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'reviews/create_ticket.html', context=context)

@login_required
def review_and_ticket_upload(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_reviews_ticket.html', context=context)

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'reviews/home.html', context={'tickets': tickets})

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'reviews/view_ticket.html', {'ticket': ticket})

@login_required
def index(request):
    template = loader.get_template('reviews/index.html')
    return HttpResponse(template.render(request=request))

@login_required
def listing(request):
    '''     albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
        message = """<ul>{}</ul>""".format("\n".join(albums)) '''
    message = "listing"
    return HttpResponse(message)

@login_required
def detail(request, album_id):
    ''' id = int(album_id) # make sure we have an integer.
    album = ALBUMS[id] # get the album with its id.
    artists = " ".join([artist['name'] for artist in album['artists']]) # grab artists name and create a string out of it.
    message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists) '''
    message = "detail"
    return HttpResponse(message)

@login_required
def search(request):
    ''' query = request.GET.get('query')
    if not query:
        message = "Aucun artiste n'est demandé"
    else:
        albums = [
            album for album in ALBUMS
            if query in " ".join(artist['name'] for artist in album['artists'])
        ]

        if len(albums) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            albums = ["<li>{}</li>".format(album['name']) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))
    '''
    message = "search"
    return HttpResponse(message)
