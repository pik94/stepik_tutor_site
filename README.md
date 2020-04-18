#### Description
This edicational project is the third task of an online [course](https://academy.stepik.org/flask). 
It's a simple web site that helps to look for a English language tutor in 
according to your demands, book classes or send a request to help in searching.

#### Install
1. Create virtualenv and activate it:
    ```shell script
    python3.7 -m venv venv && source ./venv/bin/python3
    ```
2. Install required packages:
   ```shell script
    pip install -r requirements.txt
   ```

#### Running
1.  Export necessary environment variables:
    ```shell script
    export DB_USER=user_1 DB_PASSWORD=super_secret_pass
    ```
    A list of variables:
    | Variable | Require | Default | Description|
    | ------ | ------ | ------ | ----------|
    | DB_TYPE | no | postgres | Database type. Now SQLite and PostgreSQL are supported. |
    | DB_HOST | no | localhost | A database host. |
    | DB_PORT | no | 5432 | A database port. |
    | DB_USER | yes (no no SQLite) | user | A database user. Required to be set if it's used no SQLite database. |
    | DB_PASSWORD | yes (no for SQLite) | password | A database user. Required to be set if it's used no SQLite database. |
    | DB_NAME | no (yes for SQLite) | tutordb | A database name. If you use SQLite use an absolute or relative path to the database. |
    | SERVER_NAME | no | localhost | An address where the server will be deployed. |
    | SERVER_PORT | no | 5000 | A port that the server will listen. |
    | CSRF_TOKEN| no | random | A CSRF token. |

2. Create tables
    Make sure that you created database passed via `DB_NAME`. After that, create tables typing:
    ```shell script
    flask db upgrade
    ```
   
3. Fill tables
    ```shell script
    python init_data.py
    ```

4.  For running on a production server:
    ```shell script
    python app.py
    ```

    Running in a debug mode:
    ```shell script
    python app.py -d
    ```

    To see all keys for running, type:
    ```shell script
    python app.py -h
    ```
