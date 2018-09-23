from mcstatus import MinecraftServer
from datetime import timedelta, datetime
from django.core.mail import mail_admins
from django_cron import CronJobBase, Schedule
from Daniels_Website.settings import common as settings
from pages.models import DutyShiftSource, DutyShift, MinecraftServerPing

from .google_spreadsheet import get_spreadsheet

class UpdateDutyScheduleJob(CronJobBase):
    """
    A job to periodically syncronize the model with the source (Google Spreadsheet(s)).
    """
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tools.cron.UpdateDutyScheduleJob'

    def do(self):
        "Reloads the calendar of duty shifts"
        for source in DutyShiftSource.objects.all(): # go through each of the sources
            spreadsheet = get_spreadsheet(source.spreadsheet_id, source.range)
            for i in range(0, len(spreadsheet)):
                # go through each of the date rows and add the shift
                if (len(spreadsheet[i]) > 0): # not a padding row
                    if ("Date" in spreadsheet[i][0] and len(spreadsheet) > i): # found a date heading row
                        for j in range(1, len(spreadsheet[i])): # go through each of dates for this row
                            result = {}
                            # parse the date for current day
                            result["date"] = datetime.strptime(spreadsheet[i][j], '%m/%d/%Y').strftime('%Y-%m-%d')

                            # remove any shifts for this date if there are any
                            DutyShift.objects.filter(date=result["date"]).delete()
                            print(str(i) + " " + str(j))
                            print(spreadsheet[i][j])
                            if len(spreadsheet[i + 1]) <= j: # no data for daniels for this day
                                data = ""
                            else:
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
                            result['source'] = source
                            shift = DutyShift(**result)
                            shift.save()

class UpdateServerStatusJob(CronJobBase):
    """
    A job to periodically update the known status of the Minecraft server, and alert
    admins if it is down for too long.
    """
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tools.cron.UpdateServerStatusJob'

    def do(self):
        "Updates the known status of the server."
        server = MinecraftServer(settings.MINECRAFT_SERVER_HOST)
        # create the ping and save it
        try:
            status = server.status()
            query = server.query()
            ping = MinecraftServerPing(is_online=True, 
                                status="Online", 
                                version=query.software.version,
                                latency=status.latency,
                                player_count_online=status.players.online, 
                                player_count_max=status.players.max)
        except:
            ping = MinecraftServerPing(is_online=False,
                                       status="Offline")
            # see how long the server has been down
            last_online = MinecraftServerPing.objects.filter(is_online=True).latest(field_name="date")
            if last_online and last_online.how_long_ago() == timedelta(minutes=settings.MINECRAFT_SERVER_DOWNTIME_ALERT):
                mail_admins("Minecraft server is down!",
                          "The server has been down since " + last_online.strftime('%I:%M %p'),
                          True)
        ping.save()


