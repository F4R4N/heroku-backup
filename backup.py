#!/usr/bin/python3.10

import datetime
import os
import json
import argparse

parser = argparse.ArgumentParser(prog="python backup.py", )
parser.add_argument(
    "-s", "--settings",
    help="file path that contain settings. in json format.",
    nargs='?', default="settings.json")


class CustomExceptions(Exception):
    pass


def load_settings(settings_file):
    settings = ""
    with open(settings_file, "r", encoding="utf-8") as file:
        settings = file.read()
    try:
        data = json.loads(settings)
        if data["main_path"][-1] != "/":
            data["main_path"] = data["main_path"] + "/"
        data_list = [data["app_name"], data["main_path"], data["tables"]]
    except KeyError as error:
        raise CustomExceptions(f"ERROR: {error.message} is not a valid setting key.") from error
    return data_list


def backup(app_name, main_path, tables):
    os.chdir(main_path)
    now = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    commands = {}
    os.mkdir(now)
    os.chdir(now)
    print("\u001b[34m" + "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+" + "\033[0m")

    for table in tables:
        commands[table] = f"heroku pg:psql -c \"\\copy (select * from {table}) to \'./b-{table}.csv\' with csv\" -a {app_name}"
    commands["django-dumpdata"] = f"heroku run python manage.py dumpdata -a {app_name} > b-dumpdata-python.json"

    for name, command in commands.items():
        print("\033[92m" + f"\n+++---------- '{name}' ----------+++\n" + "\033[0m")
        os.system(command)

        print("\u001b[34m" + "in: "+ "\033[0m" + f"{main_path}{now}/b-{name}.csv")
    print("\nDone.\n\u001b[34m" +
    "\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+" + "\033[0m\n")


def main():
    args = parser.parse_args()
    data = load_settings(settings_file=args.settings)
    backup(data[0], data[1], data[2])


if __name__ == '__main__':
    main()
