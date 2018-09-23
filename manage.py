import os

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Daniels_Website.settings.prod'

    import sys
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
