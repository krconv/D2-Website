from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Duty Display tool
class DutyShiftSource(models.Model):
    """
    A source for duty shifts.
    """
    spreadsheet_id = models.CharField(max_length=50, verbose_name="spreadsheet ID")
    range = models.CharField(max_length=25, verbose_name="spreadsheet range")

class DutyShift(models.Model):
    """
    A duty shift.
    """
    date = models.DateField(verbose_name="shift date")
    name = models.CharField(max_length=25, verbose_name="RA name")
    phone = models.CharField(max_length=25, blank=True, verbose_name="RA phone number")
    source = models.ForeignKey(DutyShiftSource, verbose_name="data source")

    def get_current_shift():
        "Get the currently active shift."
        hour = datetime.now().hour
        # determine which shift date we are looking for
        if (hour < 8):
            shift_date = datetime.today() - timedelta(days=1)
        elif (hour >= 21):
            shift_date = datetime.today()
        else: # no one is on duty
            shift_date = None
        # lookup a shift for the determined date
        if (shift_date):
            try:
                return DutyShift.objects.get(date=shift_date)
            except models.ObjectDoesNotExist: # no shift for this date
                return None
        else: # no shift is active
            return None

    def __str__(self):
        return self.date.strftime('%m/%d/%y') + " (%s)" % self.name;

    class Meta:
        permissions = (
            ('duty_display', "Can see the duty display"),
            ('duty_name', "Can see the name of the RA on duty"),
            ('duty_phone', "Can see the phone number of the RA on duty"),
            ('duty_room', "Can see the room of the RA on duty")
        )

# Minecraft tools
class MinecraftUser(models.Model):
    """
    A Minecraft account that is associated with a WPI user.
    """
    username = models.CharField(max_length=16, unique=True, verbose_name="in-game username")
    password = models.CharField(max_length=32, verbose_name="password")
    owner = models.ForeignKey(User, verbose_name="owner")
    banned = models.BooleanField(default=False, verbose_name="banned")

    def is_valid(self):
        "Whether the user is valid."
        if len(self.username) < 3 or len(self.username) > 16:
            return False
        for c in self.username:
            if c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-':
                return False
        return True

    def has_owner(self):
        "Returns whether this user has an owner"
        return self.owner_id is not None

    def __str__(self):
        return self.username;

    class Meta:
        permissions = (
            ('minecraft_register', "Can add a registered Minecraft user"),
        )

class MinecraftServerPing(models.Model):
    """
    Collected information about the Minecraft server that is periodically added.
    """
    is_online = models.BooleanField(verbose_name="is online")
    status = models.CharField(max_length=16, verbose_name="server status")
    latency = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="latency")
    player_count_online = models.IntegerField(default=0, verbose_name="online player count")
    player_count_max = models.IntegerField(default=0, verbose_name="maximum player count")
    date = models.DateTimeField(auto_now_add=True, verbose_name="ping date")

    def how_long_ago(self):
        "Gets a timedelta object representing how long ago this ping happened."
        return timezone.now() - self.date

    def get_latest_status():
        "Gets the latest known status of the server."
        return MinecraftServerPing.objects.latest('date')
    
    def __str__(self):
        return self.date.strftime('%m/%d/%y %H:%S') + " (%s)" % self.status;

    class Meta:
        permissions = (
            ('minecraft_status_address', "Can view the server host"),
            ('minecraft_status_status', "Can view the server status"),
            ('minecraft_status_players_count', "Can view the server's online player count"),
            ('minecraft_status_players_names', "Can view the server's online player names"),
        )

# Blog tools
class SitePost(models.Model):
    """
    A post which can be written by an author, with a title, date and body.
    """
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    
    def __str__(self):
        return self.title + " (%s)" % self.date.strftime('%m/%d/%y');