database config

# postgresql
## install database
**ubuntu**

```console
$ sudo apt install postgresql
```

## create user and database

login psql
postgres user's password is post123
```console
$ sudo -u postgres psql -p 5432
```

create database, database name is delibird
```sql
postgres=# create database delibird;
```
create user and grant creatdb privilege
```sql
create user test with password 'test123';
alter user test createdb;
```

grant to user
```sql
postgres=# grant all privileges on database delibird to test

GRANT ALL ON schema public TO test;
```


