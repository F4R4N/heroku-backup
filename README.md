# heroku-backup
a pure python app to take backup of postgresql database for django apps

```json
{
	"app_name": "movie-quote-api",
	"main_path": "/home/faran/Backup-heroku-movie-quote/",
	"tables": [
		"quote",
		"role",
		"show"
	]
}
```
should include setting like above example.

put as much database table name you have in "tables" array.

"app_name" is your heroku app name.

"main_path" is where you want to store your backup files.

all database backups are ".csv" files. but django "dumpdata" that is in ".json" format.
