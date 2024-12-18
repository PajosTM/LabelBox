from django.urls import path
from .views import upload_image, image_list, save_annotation,  annotation_page, view_annotation

urlpatterns = [
    path('upload/', upload_image, name='upload'),
    path('', image_list, name='images'),
    path('view_annotation/<int:image_id>/', view_annotation, name='view_annotation'),
    path('annotate/<int:image_id>/', annotation_page, name='annotation_page'),
    path('save-annotation/', save_annotation, name='save_annotation')
]
