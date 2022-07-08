# heroku-backup

a pure python app to take backup from postgresql database in heroku for django apps.

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

first you have to login to your heroku account from cli.

change the "settings.json" file like above example.

put as much database table name you want to backup in "tables" array.

"app_name" is your heroku app name.

"main_path" is where you want to store your backup  files in your computer.

all database backups have ".csv" format. but result of django "dumpdata" have json format.
