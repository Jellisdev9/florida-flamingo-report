"""
subscribers/views.py

Contains both the existing DRF API view (kept) and the new HTML form
subscribe view for Django templates.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Subscriber
from .serializers import SubscriberSerializer


# ── DRF API view (unchanged) ──────────────────────────────────────────────────

@api_view(["POST"])
def subscribe(request):
    email = request.data.get("email", "").lower().strip()
    if Subscriber.objects.filter(email=email).exists():
        return Response({"message": "Already subscribed."}, status=status.HTTP_200_OK)
    serializer = SubscriberSerializer(data={"email": email})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Subscribed successfully."}, status=status.HTTP_201_CREATED)


# ── Template view ──────────────────────────────────────────────────────────────

@require_POST
def subscribe_view(request):
    """
    Handles the newsletter subscription form POST from Django templates.

    Unlike the API view (which returns JSON), this view:
    1. Reads 'email' from the HTML form's POST body (not JSON)
    2. Saves the subscriber (get_or_create handles duplicates gracefully)
    3. Sets a session flag so the destination page can show "You're subscribed!"
    4. Redirects back to wherever the form was submitted from

    @require_POST ensures this view only accepts POST requests.
    A GET to /subscribe/ returns 405 Method Not Allowed automatically.

    The 'next' hidden input in every subscribe form tells us where to
    redirect after saving — e.g. "/" or "/notable-sales/".
    """
    email = request.POST.get("email", "").strip()
    # The 'next' hidden field in the form — defaults to '/' if not provided
    next_url = request.POST.get("next", "/")

    if email:
        # get_or_create returns (instance, created_bool)
        # If the email already exists, created=False and no exception is raised
        Subscriber.objects.get_or_create(email=email)
        # Store a flag in the user's session so the next page can show a
        # success message. session.pop() in the view clears it after one use.
        request.session["subscribed"] = True

    # redirect() returns a 302 response sending the browser to next_url
    return redirect(next_url)


def unsubscribe_view(request):
    """
    Handles /unsubscribe/ — a self-service page, not a link with a token.

    GET shows the "enter your email" form. POST deactivates any matching
    Subscriber and shows the same confirmation either way, whether or not
    the email was ever on the list — this avoids using the page to probe
    which emails are subscribed. No ownership verification is required
    here, matching subscribe_view's own trust model (subscribing doesn't
    require proving you own the email either).
    """
    submitted = False
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        Subscriber.objects.filter(email=email).update(is_active=False)
        submitted = True

    return render(request, "unsubscribe.html", {"submitted": submitted})
