""" ajax file
"""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.html import escape

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.utils.labels import get_data_label
from core_main_app.views.common.ajax import EditObjectModalView
import core_main_registry_app.components.data.api as data_registry_api
from core_dashboard_registry_app.views.common.forms import EditDataForm


@login_required
def switch_data_status(request):
    """switch the data status

    Returns:

    """
    try:
        data_id = request.POST.get("data_id", None)
        new_status = request.POST.get("new_status", None)
        if data_id is not None and new_status is not None:
            data = data_api.get_by_id(data_id, request.user)
            data_registry_api.set_status(data, new_status, request)
        else:
            return HttpResponseBadRequest(
                json.dumps(
                    {"message": "The data id and the new status are required"}
                ),
                content_type="application/javascript",
            )
    except exceptions.DoesNotExist as dne:
        return HttpResponseBadRequest(
            json.dumps({"message": escape(str(dne))}),
            content_type="application/json",
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            json.dumps({"message": escape(str(exception))}),
            content_type="application/javascript",
        )
    return HttpResponse(json.dumps({}), content_type="application/javascript")


@login_required
def publish(request):
    """Publish a resource.

    Returns:

    """
    try:
        data_id = request.POST.get("data_id", None)
        if data_id is not None:
            data = data_api.get_by_id(data_id, request.user)
            data_registry_api.publish(data, request.user)
            messages.add_message(
                request,
                messages.SUCCESS,
                get_data_label().capitalize() + " published with success.",
            )
        else:
            return HttpResponseBadRequest(
                json.dumps({"message": "The data id is required"}),
                content_type="application/javascript",
            )
    except exceptions.DoesNotExist as dne:
        return HttpResponseBadRequest(
            json.dumps({"message": escape(str(dne))}),
            content_type="application/json",
        )
    except AccessControlError:
        return HttpResponseBadRequest(
            json.dumps(
                {
                    "message": "You don't have enough right to perform this action."
                }
            ),
            content_type="application/json",
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            json.dumps({"message": escape(str(exception))}),
            content_type="application/javascript",
        )
    return HttpResponse(json.dumps({}), content_type="application/javascript")


@method_decorator(login_required, name="dispatch")
class EditDataView(EditObjectModalView):
    """EditDataView"""

    form_class = EditDataForm
    model = Data
    success_message = "Title edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            data_api.upsert(self.object, self.request)
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_success_url(self):
        return self.request.META["HTTP_REFERER"]
