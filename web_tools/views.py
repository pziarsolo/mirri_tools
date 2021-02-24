from web_tools.forms import ValidationUploadForm
from django.shortcuts import render
from django.template.context_processors import csrf
from django.shortcuts import render
from pathlib import Path
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
            print('valid')
            fhand = form.cleaned_data["file"]
            error_log = validate_mirri_excel(fhand)

            errors = [error for errors in error_log.errors.values()
                      for error in errors]

            valid = True if not errors else False
            context['fname'] = fhand.name
            context["valid"] = valid
            context["errors"] = errors[:100]
            context["more_errors"] = len(errors[100:])

            # error_log.write(Path("/dev/null"))

        context["validation_done"] = True

    else:
        form = ValidationUploadForm()
        context["validation_done"] = False
    context["form"] = form

    template = "validator.html"
    content_type = None
    return render(request, template, context=context, content_type=content_type)


def index(request):
    return render(request, "tools_index.html")
