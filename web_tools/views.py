from web_tools.forms import ValidationUploadForm
from django.shortcuts import render
from django.template.context_processors import csrf

from mirri.validation.mirri_excel import validate_mirri_excel


from openpyxl import load_workbook
from io import BytesIO

# Create your views here.
def validation_view(request):
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        request_data = request.POST
    elif request.method == "GET":
        request_data = request.GET
    else:
        request_data = None
    form = None

    if request_data:
        form = ValidationUploadForm(request_data, request.FILES)
        if form.is_valid():
            fhand = form.cleaned_data["file"]
            error_log = validate_mirri_excel(fhand)
            context["errors"] = error_log.errors
            for key, errors in error_log.errors.items():
                print(errors[0].data)
            # errorlog_.write(path_to_tmp_pdf)
        context["search_done"] = True

    else:
        form = ValidationUploadForm()
        context["search_done"] = False
    context["form"] = form

    template = "validator.html"
    content_type = None
    return render(request, template, context=context, content_type=content_type)
