from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Image, Annotation
from django.urls import reverse  # Import reverse


def upload_image(request):
    if request.method == 'POST' and request.FILES['image_file']:
        # Get the image from the form
        title = request.POST.get('title')  # Get the title from the form
        image_file = request.FILES['image_file']  # Get the uploaded file

        # Create a new Image instance and save it to the database
        image = Image.objects.create(title=title, image_file=image_file)

        # Redirect to the annotation page with the newly uploaded image's ID
        return redirect(reverse('annotation_page', kwargs={'image_id': image.id}))

    return render(request, 'annotation/upload.html')


def image_list(request):
    images = Image.objects.all()
    return render(request, 'annotation/images.html', {'images': images})

@csrf_exempt
def save_annotation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract image_id and annotation data (bounding boxes)
            image_id = data.get('image_id')
            annotation_data = data.get('annotation')

            # Fetch the corresponding Image object
            image = Image.objects.get(id=image_id)

            # Check if an annotation already exists for this image
            existing_annotation = Annotation.objects.filter(image=image).first()

            if existing_annotation:
                # Update the existing annotation
                existing_annotation.annotation_data = annotation_data
                existing_annotation.save()
                message = 'Annotation updated successfully!'
            else:
                # Create a new annotation
                Annotation.objects.create(image=image, annotation_data=annotation_data)
                message = 'Annotation saved successfully!'

            return JsonResponse({'message': message}, status=200)

        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def annotation_page(request, image_id):
    # Fetch the image to annotate
    image = get_object_or_404(Image, id=image_id)  # Replace with logic to fetch the correct image
    return render(request, 'annotation/annotate.html', {'image': image})

def view_annotation(request, image_id):
    # Fetch the image and its annotation
    image = get_object_or_404(Image, id=image_id)
    annotations = Annotation.objects.filter(image=image)

    # Pass the image and annotations to the template
    return render(request, 'annotation/view_annontate.html', {
        'image': image,
        'annotations': annotations,
    })