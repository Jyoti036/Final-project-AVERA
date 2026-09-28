from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("adoption/", views.adoption_list, name="adoption_list"),
    path("adoption/<int:pk>/", views.adoption_detail, name="adoption_detail"),
    path("awareness/", views.awareness_list, name="awareness_list"),
    path("awareness/<int:pk>/", views.awareness_detail, name="awareness_detail"),
    path("organizations/", views.organization_list, name="organization_list"),
    path("organizations/<int:pk>/", views.organization_detail, name="organization_detail"),
    path("children/", views.child_list, name="child_list"),
    path("children/<int:pk>/", views.child_detail, name="child_detail"),
    path("stories/", views.story_list, name="story_list"),
    path("stories/<int:pk>/", views.story_detail, name="story_detail"),
    path("wishlist/", views.wishlist_list, name="wishlist_list"),
    path("wishlist/create/", views.wishlist_create, name="wishlist_create"),
    path("gifts/create/", views.gift_create, name="gift_create"),
    path("gifts/<int:pk>/", views.gift_detail, name="gift_detail"),
    path("gifts/<int:gift_id>/feedback/", views.feedback_create, name="feedback_create"),
    path("faq/", views.faq, name="faq"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
