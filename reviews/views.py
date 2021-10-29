from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from itertools import chain
from django.template import loader, RequestContext

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
        edit_ticket = forms.TicketForm(request.POST, request.FILES, instance=ticket)
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
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
    return redirect('my_posts')


@login_required
def edit_review(request, ticket_id, review_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review = get_object_or_404(models.Review, id=review_id)
    edit_review = forms.ReviewForm(instance=review)
    delete_review = forms.DeleteReviewForm()
    if request.user == review.user:
        if request.method == 'POST':
            print(request.POST)
            edit_review = forms.ReviewForm(request.POST, instance=review)
            if edit_review.is_valid():
                edit_review.save()
                return redirect('home')
            if 'delete_review' in request.POST:
                delete_review = forms.DeleteReviewForm(request.POST)
                print(delete_review)
                if delete_review.is_valid():
                    review.delete()
                    return redirect('home')
        else:
            context = {
                'ticket': ticket,
                'edit_review': edit_review,
                'delete_review': delete_review,
            }
            return render(request, 'reviews/edit_review.html', context=context)
    context = {
        'ticket': ticket,
        'review': review,
    }
    return render(request, 'reviews/view_review.html', context=context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if request.user == review.user:
        if request.method == 'POST':
            review.delete()
    return redirect('my_posts')


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
        'rating': review.rating,
    }
    return render(request, 'reviews/view_review.html', context=context)

@login_required
def view_follows(request):
    # followers = get_object_or_404(models.UserFollows, id=request.user.id)
    followers = models.UserFollows.objects.all()
    context = {
        'followers': followers,
    }
    return render(request, 'reviews/view_follows.html', context=context)

@login_required
def add_follow(request):
    users = User.objects.all()
    follow = models.UserFollows.objects.filter(user=request.user.id)
    print(users)
    print(follow)
    if request.method == 'POST':
        try:
            form = request.POST
            user1 = get_object_or_404(User, username=request.user.username)
            user2 = get_object_or_404(User, username=form["follow_user"])
            if user1 == user2:
                return redirect(view_follows)
            models.UserFollows.objects.create(user=user1,
                                    followed_user=user2)
        except:
            return redirect(view_follows)
    return redirect(view_follows)

@login_required
def delete_follows(request, follower_id):
    followed = get_object_or_404(models.UserFollows, id=follower_id)
    followed.delete()
    return redirect(view_follows)

@login_required
def review_and_ticket_upload(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        print(ticket_form)
        print(request.FILES)
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
