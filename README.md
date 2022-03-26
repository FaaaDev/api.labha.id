# Accounting API

This project using for support cross paltform (multi-platform) Accounting itungin application.
This application made by Python using Flask framework. Make sure you has install [Python](https://www.python.org/) before running this application.

## Install Required Library

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
Or using pip3 for python3.

```bash
pip3 install -r requirements.txt
```

## Configure

You can change host and port as you want.
```python
from main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3003)
```

Make sure you also change database configuration.

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/YOUR_DB_NAME'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

## Running Application

You can run this project directly using Python.

```bash
python app.py
```
Or using Python3
```bash
python3 app.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
