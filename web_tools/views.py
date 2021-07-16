import string
import random
import os.path
from typing import OrderedDict
import uuid
from datetime import datetime

from django.template.loader import get_template
from django.shortcuts import render
from django.template.context_processors import csrf
from django.conf import settings as global_settings

from xhtml2pdf import pisa

from mirri.validation.excel_validator import validate_mirri_excel
from mirri.validation.error_logging.error import Entity

from web_tools import settings
from web_tools.forms import ValidationUploadForm
from web_tools.send_mail import send_mail


def random_choice():
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=8))


def render_to_pdf(template_name, context, out_fhand):
    template = get_template(template_name)
    html = template.render(context)
    # print(html)
    return pisa.CreatePDF(html.strip(), dest=out_fhand)


def validation_view(request):
    context = {}
    context.update(csrf(request))
    if request.method == "GET":
        request_data = request.GET
    elif request.method == "POST":
        request_data = request.POST
    else:
        request_data = None
    form = None

    if request_data:
        form = ValidationUploadForm(request_data, request.FILES)
        if form.is_valid():
            fhand = form.cleaned_data["file"]
            fname = fhand.name
            do_upload = form.cleaned_data['do_upload']
            version = '20200601'

            error_log = validate_mirri_excel(fhand, version=version)
            all_errors = error_log.get_errors()
            total_num_errors = sum(len(errors) for errors in all_errors.values())
            errors_filtered_by_size = prepare_dict_to_show(all_errors,
                                                           limit=settings.NUM_ERROR_LIMIT)

            uploaded = False
            valid = not total_num_errors

            if valid and do_upload:
                out_dir = settings.VALID_EXCEL_UPLOAD_DIR
                date_uuid = datetime.now().strftime('%Y%m%d-%H:%M:%S')
                path = out_dir / f'{date_uuid}_{fname}'

                with path.open('wb') as out_fhand:
                    fhand.seek(0)
                    out_fhand.write(fhand.read())
                uploaded = True

                if settings.NOTIFICATION_RECEIVERS:
                    send_mail(settings.NOTIFICATION_RECEIVERS, path.name)

            context['uploaded'] = uploaded
            context['fname'] = fname
            context["valid"] = valid
            context["all_errors"] = errors_filtered_by_size
            context['total_errors'] = total_num_errors
            context['error_limited_to'] = settings.NUM_ERROR_LIMIT

            if not valid:
                _uuid = str(uuid.uuid4())
                error_fname = f'out_pdf/{_uuid}mirri_validator_output.pdf'

                error_pdf_fpath = os.path.join(global_settings.MEDIA_ROOT,
                                               error_fname)

                error_pdf_url = global_settings.MEDIA_URL + error_fname

                with open(error_pdf_fpath, 'wb') as out_fhand:
                    result = render_to_pdf("validation_pdf_output.html", context,
                                           out_fhand)
                if result.err == 0:
                    pdf_creation_error = True
                    context['error_pdf_url'] = error_pdf_url

        context["validation_done"] = True

    else:
        form = ValidationUploadForm()
        context["validation_done"] = False
    context["form"] = form

    template = "validation_html_output.html"
    content_type = None
    return render(request, template, context=context, content_type=content_type)

def prepare_dict_to_show(dictionary, limit):
    new_dict = OrderedDict()
    remaining = limit
    for key, values in dictionary.items():
        new_values = values[:remaining] if len(values) >= remaining else values
        remaining -= len(new_values)
        key = Entity(key).name
        new_dict[key] = new_values
        if remaining <= 0:
            break
    return new_dict


def index(request):
    return render(request, "index.html")


def tool_list_view(request):
    return render(request, "tools_index.html")
