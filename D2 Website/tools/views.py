from django_ajax.decorators import ajax

from . import duty_display

@ajax
def duty_tool(request):
    duty_info = duty_display.name_on_duty()
    # remove the number if the user isn't authenticated
    if not request.user.is_authenticated():
        del duty_info['phone'];
    return duty_info;