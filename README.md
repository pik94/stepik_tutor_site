#### Description
This project is the third task of an online [course](https://academy.stepik.org/flask)
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
Initialize data:
```shell script
python init_db.py
```

For running type:
```shell script
python app.py --host 0.0.0.0 --port 8080
```
To see all keys for running, type:
```shell script
python app.py -h
```
