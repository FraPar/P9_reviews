from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from itertools import chain
from django.template import loader, RequestContext

# from .models import ALBUMS # commentez cette ligne

# Create your views here.

from . import forms, models
from authentication.models import User

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
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_ticket = forms.TicketForm(instance=ticket)
    delete_ticket = forms.DeleteTicketForm()
    if request.method == 'POST':
        edit_ticket = forms.TicketForm(request.POST, instance=ticket)
        if edit_ticket.is_valid():
            edit_ticket.save()
            return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_ticket = forms.DeleteTicketForm(request.POST)
            if delete_ticket.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_ticket': edit_ticket,
        'delete_ticket': delete_ticket,
    }
    return render(request, 'reviews/edit_ticket.html', context=context)

@login_required
def edit_review(request, ticket_id, review_id):
    # request.user (permet d'acceder a l'instance de l'user et son ID etc...)
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.ReviewForm(instance=review)
    delete_review = forms.DeleteReviewForm()
    if request.user == ticket.user:
        if request.method == 'POST':
            edit_review = forms.ReviewForm(request.POST, instance=review)
            if edit_review.is_valid():
                edit_review.save()
                return redirect('home')
            if 'delete_review' in request.POST:
                delete_review = forms.DeleteReviewForm(request.POST)
                if delete_review.is_valid():
                    review.delete()
                    return redirect('home')
    else:
        context = {
            'ticket': ticket,
            'review': review,
        }
        return render(request, 'reviews/view_review.html', context=context)
    context = {
        'ticket': ticket,
        'edit_review': edit_review,
        'delete_review': delete_review,
    }
    return render(request, 'reviews/edit_review.html', context=context)

@login_required
def review_upload(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if any([review_form.is_valid()]):
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'ticket': ticket,
        'review_form': review_form,
    }
    return render(request, 'reviews/create_review.html', context=context)

@login_required
def view_review(request, ticket_id, review_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = get_object_or_404(models.Review, id=review_id)
    context = {
        'ticket': ticket,
        'review': review,
    }
    return render(request, 'reviews/view_review.html', context=context)

@login_required
def view_follows(request):
    # followers = get_object_or_404(models.UserFollows, id=request.user.id)
    follow_form = forms.FollowedUserForm()
    followers = models.UserFollows.objects.all()
    context = {
        'followers': followers,
        'follow_form': follow_form,
    }
    return render(request, 'reviews/view_follows.html', context=context)

@login_required
def add_follow(request):
    print(request.user.id)
    user1 = get_object_or_404(User, username="admin")
    user2 = get_object_or_404(User, username="superadmin")

    models.UserFollows.objects.create(user=user1,
                             followed_user=user2)
    return redirect(view_follows)

@login_required
def delete_follows(request, follower_id):
    followed = get_object_or_404(models.UserFollows, id=follower_id)
    followed.delete()
    return redirect(view_follows)

@login_required
def search(request):
    query = request.GET.get('q')
    try:
        query = int(query)
    except ValueError:
        query = None
        results = None
    if query:
        results = models.UserFollows.objects.get(uid=query)
    context = RequestContext(request)
    return render('view_follows.html', {"results": results,}, context_instance=context)

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
    reviews = models.Review.objects.all()
    
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'all_tickets': tickets,
        'page_obj': page_obj,
    }

    return render(request, 'reviews/home.html', context=context)

@login_required
def my_posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    paginator = Paginator(tickets_and_reviews, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'all_tickets': tickets,
        'page_obj': page_obj,
    }

    return render(request, 'reviews/flux.html', context=context)

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
