from django.urls import path, include


urlpatterns = [

    path('', include('app_user.urls')),
    path('', include('app_exhibition_visit.urls')),
    path('', include('app_news_information.urls')),
    path('', include('app_historical_figures.urls')),

]