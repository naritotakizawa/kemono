from django.shortcuts import redirect
from django.views import generic
from .forms import UploadForm
from .models import Image
from deep.main import predict


class ImageList(generic.ListView):
    model = Image


class ImageForm(generic.FormView):
    form_class = UploadForm
    template_name = 'image/image_form.html'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        result_img, char_names = predict(file)
        image_model = Image(file=result_img, names=char_names)
        image_model.save()
        return redirect('image:list')