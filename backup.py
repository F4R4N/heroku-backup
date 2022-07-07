#!/usr/bin/python3.9

import datetime
import os
import json
import argparse

parser = argparse.ArgumentParser(prog="python backup.py", )
parser.add_argument("-s", "--settings", help="file path that contain settings. in json format.", nargs='?', default="settings.json")


class CustomExceptions(Exception):
	pass


def load_settings(settings_file):
	settings = ""
	with open(settings_file, "r") as file:
		settings = file.read()
	try:
		data = json.loads(settings)
		if data["main_path"][-1] != "/":
			data["main_path"] = data["main_path"] + "/"
		data_list = [data["app_name"], data["main_path"], data["tables"]]
	except KeyError as error:
		raise CustomExceptions("ERROR: {0} is not a valid setting key.".format(error.message))
	return data_list


def backup(app_name, main_path, tables):
	os.chdir(main_path)
	now = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
	commands = {}
	os.mkdir(now)
	os.chdir(now)
	print("\u001b[34m" + "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+" + "\033[0m")

	for table in tables:
		commands[table] = "heroku pg:psql -c \"\\copy (select * from {0}) to \'./b-{0}.csv\' with csv\" -a {1}".format(table, app_name)
	commands["django-dumpdata"] = "heroku run python manage.py dumpdata -a {} | json_pp > b-dumpdata-python.json".format(app_name)

	for command in commands:
		print("\033[92m" + f"\n+++---------- '{command}' ----------+++\n" + "\033[0m")
		os.system(commands[command])

		print("\u001b[34m" + "in: "+ "\033[0m" + "{0}{1}/b-{2}.csv".format(main_path, now, command))
	print("\nDone.\n\u001b[34m" + "\n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+" + "\033[0m\n")


def main():
	args = parser.parse_args()
	data = load_settings(settings_file=args.settings)
	backup(data[0], data[1], data[2])


if __name__ == '__main__':
	main()
