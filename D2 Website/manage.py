#!/home/d2/D2_Website/env/bin/python3.4
import os
import sys

# because windows uses capitalized directories, need to decapitalize them when on linux
if ('linux' in sys.platform):
    for dirname in os.listdir('env'):
        if (dirname[0].isupper()):
            os.rename(os.path.join('env', dirname), os.path.join('env', dirname.lower()));

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d2.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
