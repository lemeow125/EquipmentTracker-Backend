from django.urls import path, include

urlpatterns = [
    path('accounts/', include('djoser.urls'))
]
