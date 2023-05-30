from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "dashboard"

urlpatterns = [
    path("", login_required(views.index), name="index"),
    path("search_detail/<slug>", login_required(views.SearchLeadsDetail.as_view()), name="search_detail"),
    path("search_form/", login_required(views.search_form), name="search_form"),
    path('delete_search/<slug:slug>/', login_required(views.delete_search), name='delete_search'),
    path('delete_lead/<slug:slug>/', login_required(views.delete_lead), name='delete_lead'),
    path('save_to_json_leads/<slug:slug>', login_required(views.save_to_json_leads), name='save_to_json_leads'),
    path('save_to_csv_leads/<slug:slug>', login_required(views.save_to_csv_leads), name='save_to_csv_leads'),
    path('star_lead/<slug:slug>/', login_required(views.star_lead), name='star_lead'),
]
