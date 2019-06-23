# Pymongo Docker

## Hydrating Mongo from CSV

```bash
$ mongoimport -d mydb -c mycol --type csv --file /tmp/data.csv --headerline
```