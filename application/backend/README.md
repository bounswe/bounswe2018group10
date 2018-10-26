# BACKEND

## Enter correct directory
```
cd bounswe2018group10/application/backend
```

### Create a virtual environment*
```
virtualenv myvenv
```

### Activate virtual environment
```
source myvenv/bin/activate
```

### Enter project directory
```
cd freelancer-project
```

### Install requirements
```
pip install -r requirements.txt
```

### Create an empty database
```
python manage.py migrate
```

### Run server
```
python manage.py runserver
```

<p>You can access the server via http://localhost:8000/</p>

### Important Notes
<i>Creating a virtual environment isn't mandatory but it is highly recommended. If you don't have it on your computer, you can download it with ```pip install virtualenv``` command. If you don't use just skip 2nd and 3rd steps.</i>

<i> If you have both 2nd and 3rd version of python in your computer, you should use ```pip3``` and ```python3``` commands all the time. However if you download in virtual environment using python and pip is fine. But be careful, you should still use ```pip3``` for installing virtualenv. </i>



