# Setup
To initialize a project enviroment create new projectfolder & `cd` into it

```
>> python3 -m venv venv
```

use terminal to start `venv`

```
>> source venv/bin/activate (linux)
```

download the packages 

```
>> pip install google-cloud-firestore
```

after installing all packages create `requirements.txt`

```
>> pip freeze > requirements.txt
```

if having a `requirements.txt` install dependencies using

```
>> python -m pip install -r requirements.txt
```
