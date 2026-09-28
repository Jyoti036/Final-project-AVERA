from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, GiftForm, FeedbackForm, WishlistForm
from .models import AdoptionInformation, AwarenessContent, CareOrganization, Child, SuccessStory, Wishlist, Gift, Feedback, FAQ, Notification

def home(request):
    context = {
        "stories": SuccessStory.objects.all()[:3],
        "awareness": AwarenessContent.objects.all()[:3],
        "organizations": CareOrganization.objects.filter(verification_status="verified")[:3],
        "wishlists": Wishlist.objects.filter(status__in=["Open","Partially fulfilled"])[:3],
    }
    return render(request, "main/home.html", context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to AVERA!")
            return redirect("dashboard")
    else: form = RegisterForm()
    return render(request, "main/register.html", {"form": form})

@login_required
def dashboard(request):
    gifts = request.user.gifts.select_related("organization")
    notifications = request.user.notifications.all()[:8]
    return render(request, "main/dashboard.html", {"gifts": gifts, "notifications": notifications})

def adoption_list(request):
    return render(request, "main/adoption_list.html", {"items": AdoptionInformation.objects.all()})

def adoption_detail(request, pk):
    return render(request, "main/adoption_detail.html", {"item": get_object_or_404(AdoptionInformation, pk=pk)})

def awareness_list(request):
    q = request.GET.get("q","").strip()
    items = AwarenessContent.objects.all()
    if q: items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, "main/awareness_list.html", {"items": items, "q": q})

def awareness_detail(request, pk):
    return render(request, "main/awareness_detail.html", {"item": get_object_or_404(AwarenessContent, pk=pk)})

def organization_list(request):
    return render(request, "main/organization_list.html", {"items": CareOrganization.objects.filter(verification_status="verified")})

def organization_detail(request, pk):
    org = get_object_or_404(CareOrganization, pk=pk, verification_status="verified")
    return render(request, "main/organization_detail.html", {"org": org, "wishlists": org.wishlists.filter(status__in=["Open","Partially fulfilled"])})

def child_list(request):
    return render(request, "main/child_list.html", {"items": Child.objects.filter(organization__verification_status="verified")})

def child_detail(request, pk):
    child = get_object_or_404(Child, pk=pk, organization__verification_status="verified")
    return render(request, "main/child_detail.html", {"child": child, "milestones": child.milestones.all()[:5]})

def story_list(request):
    return render(request, "main/story_list.html", {"items": SuccessStory.objects.all()})

def story_detail(request, pk):
    return render(request, "main/story_detail.html", {"item": get_object_or_404(SuccessStory, pk=pk)})

def wishlist_list(request):
    return render(request, "main/wishlist_list.html", {"items": Wishlist.objects.filter(status__in=["Open","Partially fulfilled"]).select_related("organization")})

@login_required
def wishlist_create(request):
    if request.method == "POST":
        form = WishlistForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.wishlist_id = "WL-" + uuid4().hex[:8].upper()
            item.save()
            messages.success(request, "Wishlist published.")
            return redirect("wishlist_list")
    else: form = WishlistForm()
    return render(request, "main/form.html", {"form": form, "title": "Create a Wishlist", "button": "Publish Wishlist"})

@login_required
def gift_create(request):
    initial = {}
    org = request.GET.get("organization")
    if org: initial["organization"] = org
    if request.method == "POST":
        form = GiftForm(request.POST)
        if form.is_valid():
            gift = form.save(commit=False)
            gift.gift_id = "GF-" + uuid4().hex[:8].upper()
            gift.donor = request.user
            gift.save()
            Notification.objects.create(notification_id="NT-"+uuid4().hex[:8].upper(), user=request.user, notification_type="Gift", message=f"Gift {gift.gift_id} was created and marked Sent.")
            messages.success(request, "Your support has been recorded. You can track it from your dashboard.")
            return redirect("gift_detail", pk=gift.pk)
    else: form = GiftForm(initial=initial)
    return render(request, "main/form.html", {"form": form, "title": "Send a Gift", "button": "Send Gift"})

@login_required
def gift_detail(request, pk):
    gift = get_object_or_404(Gift.objects.select_related("organization"), pk=pk)
    if gift.donor != request.user and not request.user.is_staff: return redirect("dashboard")
    return render(request, "main/gift_detail.html", {"gift": gift})

@login_required
def feedback_create(request, gift_id):
    gift = get_object_or_404(Gift, pk=gift_id, donor=request.user)
    if hasattr(gift, "feedback"):
        messages.info(request, "Feedback has already been submitted for this gift.")
        return redirect("gift_detail", pk=gift.pk)
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.feedback_id = "FB-" + uuid4().hex[:8].upper()
            fb.gift = gift
            fb.save()
            Notification.objects.create(notification_id="NT-"+uuid4().hex[:8].upper(), user=request.user, notification_type="Feedback", message=f"Feedback for {gift.gift_id} is pending verification.")
            messages.success(request, "Thank you. Your feedback is now pending verification.")
            return redirect("gift_detail", pk=gift.pk)
    else: form = FeedbackForm()
    return render(request, "main/form.html", {"form": form, "title": "Submit Gift Feedback", "button": "Submit Feedback"})

def faq(request):
    return render(request, "main/faq.html", {"items": FAQ.objects.all()})

def is_staff(user): return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def admin_dashboard(request):
    context = {
        "orgs": CareOrganization.objects.count(),
        "children": Child.objects.count(),
        "gifts": Gift.objects.count(),
        "pending_feedback": Feedback.objects.filter(verification_status="Pending").count(),
        "pending_orgs": CareOrganization.objects.filter(verification_status="pending").count(),
        "wishlists": Wishlist.objects.count(),
    }
    return render(request, "main/admin_dashboard.html", context)
