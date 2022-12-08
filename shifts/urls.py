from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('new/',views.ArrangementCreateView.as_view(),name="CreateArrangement"),
    path('new/fill<int:pk>',views.form2,name="fill"),
    path('arrangements/',views.ArrangementListView.as_view(),name="list"),
    path('arrangements/<int:pk>',views.detailView,name="detail")

]
