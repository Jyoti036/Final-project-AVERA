from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    USER_TYPES = [("supporter", "Supporter"), ("admin", "Admin")]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="supporter")
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    password_note = models.CharField(max_length=255, blank=True)

    def __str__(self): return self.name

class CareOrganization(models.Model):
    verification_choices = [("pending","Pending"),("verified","Verified"),("rejected","Rejected")]
    organization_id = models.CharField(max_length=30, unique=True)
    organization_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    description = models.TextField()
    verification_status = models.CharField(max_length=20, choices=verification_choices, default="pending")
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to="organizations/", blank=True, null=True)

    class Meta: ordering = ["organization_name"]

    def __str__(self): return self.organization_name

class Child(models.Model):
    gender_choices = [("Female","Female"),("Male","Male"),("Other","Other")]
    status_choices = [("Available","Available"),("Not available","Not available")]
    organization = models.ForeignKey(CareOrganization, on_delete=models.CASCADE, related_name="children")
    child_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, choices=gender_choices)
    description = models.TextField()
    health_status = models.CharField(max_length=255, blank=True)
    adoption_status = models.CharField(max_length=30, choices=status_choices, default="Available")
    photo = models.ImageField(upload_to="children/", blank=True, null=True)

    class Meta: ordering = ["name"]

    def __str__(self): return self.name

class AdoptionInformation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField()
    required_documents = models.TextField()
    adoption_process = models.TextField()
    contact_information = models.TextField(blank=True)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self): return reverse("adoption_detail", args=[self.pk])
    def __str__(self): return self.title

class AwarenessContent(models.Model):
    content_types = [("article","Article"),("guide","Guide"),("myth","Myth & Fact"),("event","Event")]
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=content_types, default="article")
    image = models.ImageField(upload_to="awareness/", blank=True, null=True)
    publication_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta: ordering = ["-publication_date"]

    def __str__(self): return self.title

class SuccessStory(models.Model):
    title = models.CharField(max_length=200)
    story_description = models.TextField()
    image = models.ImageField(upload_to="stories/", blank=True, null=True)
    publication_date = models.DateField(auto_now_add=True)
    organization = models.ForeignKey(CareOrganization, on_delete=models.SET_NULL, null=True, blank=True, related_name="success_stories")

    class Meta: ordering = ["-publication_date"]

    def __str__(self): return self.title

class Gift(models.Model):
    gift_types = [("Food","Food"),("Clothes","Clothes"),("Education","Education"),("Medicine","Medicine"),("Other","Other")]
    statuses = [("Sent","Sent"),("Received","Received"),("Delivered","Delivered"),("Used","Used")]
    gift_id = models.CharField(max_length=30, unique=True)
    gift_type = models.CharField(max_length=30, choices=gift_types)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=statuses, default="Sent")
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gifts")
    organization = models.ForeignKey(CareOrganization, on_delete=models.CASCADE, related_name="gifts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-created_at"]

    def __str__(self): return self.gift_id

class Feedback(models.Model):
    verification_choices = [("Pending","Pending"),("Verified","Verified"),("Rejected","Rejected")]
    feedback_id = models.CharField(max_length=30, unique=True)
    gift = models.OneToOneField(Gift, on_delete=models.CASCADE, related_name="feedback")
    message = models.TextField()
    photo = models.ImageField(upload_to="feedback/", blank=True, null=True)
    feedback_date = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(max_length=20, choices=verification_choices, default="Pending")

    def __str__(self): return self.feedback_id

class Wishlist(models.Model):
    priority_choices = [("Low","Low"),("Medium","Medium"),("High","High")]
    status_choices = [("Open","Open"),("Partially fulfilled","Partially fulfilled"),("Fulfilled","Fulfilled")]
    wishlist_id = models.CharField(max_length=30, unique=True)
    organization = models.ForeignKey(CareOrganization, on_delete=models.CASCADE, related_name="wishlists")
    title = models.CharField(max_length=200)
    description = models.TextField()
    item_name = models.CharField(max_length=120)
    quantity_needed = models.PositiveIntegerField(default=1)
    quantity_received = models.PositiveIntegerField(default=0)
    priority = models.CharField(max_length=20, choices=priority_choices, default="Medium")
    status = models.CharField(max_length=30, choices=status_choices, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ["-created_at"]

    def __str__(self): return self.title

    @property
    def remaining(self):
        return max(self.quantity_needed - self.quantity_received, 0)

class MilestoneUpdate(models.Model):
    update_id = models.CharField(max_length=30, unique=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="milestones")
    title = models.CharField(max_length=200)
    description = models.TextField()
    update_date = models.DateField()
    photo = models.ImageField(upload_to="milestones/", blank=True, null=True)

    class Meta: ordering = ["-update_date"]

class FAQ(models.Model):
    faq_id = models.CharField(max_length=30, unique=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)

    class Meta: ordering = ["category", "question"]

    def __str__(self): return self.question

class Notification(models.Model):
    notification_types = [("Gift","Gift"),("Feedback","Feedback"),("Wishlist","Wishlist"),("General","General")]
    notification_id = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=notification_types, default="General")
    message = models.CharField(max_length=255)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta: ordering = ["-notification_date"]

    def __str__(self): return self.message
