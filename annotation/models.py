from django.db import models

# Create your models here.
from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    image_file = models.ImageField(upload_to='images/')  # Upload images to "media/images" folder
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Annotation(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="annotations")
    annotation_data = models.JSONField()  # Store bounding boxes, labels, etc., as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Annotation for {self.image.title}"
