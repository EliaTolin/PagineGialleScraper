from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'PagineGialleScraper Administrator'
admin.site.site_title = 'PagineGialleScraper Administrator'
admin.site.index_title = 'PagineGialleScraper'

urlpatterns = [
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

