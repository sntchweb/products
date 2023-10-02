from django.urls import path

from api.views import ProductsLessonsView, ProductsView, StatisticsView

urlpatterns = [
    path('product/<int:product_id>/', ProductsView.as_view()),
    path('lessons/', ProductsLessonsView.as_view()),
    path('statistics/', StatisticsView.as_view()),
]
