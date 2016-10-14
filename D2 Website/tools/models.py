from datetime import date
from django.db import models
from .google_spreadsheet import get_spreadsheet

# Duty Display tool
class DutyDisplay(models.Model):
    """
    A tool which stores information about which RA is on duty.
    """
    spreadsheet_id=models.CharField(max_length=50, verbose_name="spreadsheet ID")
    range=models.CharField(max_length=25, verbose_name="spreadsheet range")

    def reload(self):
        "Reloads the calendar of duty shifts"
        spreadsheet = get_spreadsheet(spreadsheet_id, sheet_range)
        for i in range(0, len(spreadsheet)):
            # go through each of the date rows and add the shift
            if (len(spreadsheet[i]) > 0): # not a padding row
                if ("Date" in spreadsheet[i][0]):
                    for j in range(1, len(spreadsheet[i])):
                        result = { }
                        result["date"] = spreadsheet[i][j]
                        data = spreadsheet[i + 1][j].replace('(', '').replace(')', '').strip() # the duty data for daniels
                        # parse the duty for a phone number and name
                        if (len(data) == 0): # no one is on duty
                            continue
                        elif (data[-5] == "x"): # a singular person is on with a WPI phone
                            result["name"] = data[:-6]
                            result["phone"] = "508-831-" + data[-4:]
                        elif (len(data) > 12 and '-' in data[-12:] and not "All" in data): # a singular person with a cell phone
                            result["name"] = data[:-13]
                            result["phone"] = data[-12:]
                        else: # multiple people 
                            result["name"] = data

                        # remove any shifts for this date if there is any
                        DutyShift.objects.filter(date=result["date"]).remove()
                        shift = DutyShift(**result)
                        shift.save()


class DutyShift(models.Model):
    """
    A duty shift.
    """
    date=models.DateField(verbose_name="shift date")
    name=models.CharField(max_length=25, verbose_name="RA name")
    phone=models.CharField(max_length=25, blank=True, verbose_name="phone")
