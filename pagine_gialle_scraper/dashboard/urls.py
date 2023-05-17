from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("search_detail/<slug>", views.SearchLeadsDetail.as_view(), name="search_detail"),
    path("search_form/", views.search_form, name="search_form"),
    path('delete_search/<slug:slug>/', views.delete_search, name='delete_search'),
    path('save_to_json_leads/<slug:slug>', views.save_to_json_leads, name='save_to_json_leads'),
    path('save_to_csv_leads/<slug:slug>', views.save_to_csv_leads, name='save_to_csv_leads'),
]
