from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core Apps
    path('', include('dashboard.urls')),  # Main landing page/dashboard
    path('accounts/', include('accounts.urls')),  # User profile, login/logout/register etc.
    path('transactions/', include('transactions.urls')),
    path('budgets/', include('budgets.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('insights/', include('insights.urls')),

    # API
    path('api/', include('api.urls')),

    # JWT Token Auth endpoints (optional, for API/mobile auth)
    path('api/token/', 
         include('rest_framework_simplejwt.urls')),  # Provides /token/ and /token/refresh/
]

# Serve media files and static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)