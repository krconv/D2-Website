from datetime import date
from django_ajax.decorators import ajax
from .models import DutyShift

@ajax
def duty_tool(request):
    duty_info = {}
    shift = DutyShift.objects.filter(date=date.today())
    if (shift.exists()):
        shift = shift.first()
        duty_info["name"] = shift.name
        if request.user.is_authenticated() and len(shift.phone) > 0:
            duty_info['phone'] = shift.phone;
    else:
        duty_info["info"] = "No RA On Duty"
    return duty_info;