# audio_files_api
CRUD Backend for Audio Files

## Project setup
Before going through the steps make sure you have the following pre-installed

### Prerequisite
1. Python 3.6+
2. Virtualenv


Make sure to download/clone this repository and navigate to the folder in yout terminal. Now follow the indtructions below

1. Create the virtual environment.
```
    virtualenv /path/to/venv --python=/path/to/python3
```
You can find out the path to your `python3` interpreter with the command `which python3`.

2. Activate the environment and install dependencies. <os-platform> is a placeholder for windows/linux.
    - #### Linux
    ```
        source /path/to/venv/bin/activate
        pip install -r requirements\dev.<os-platform>.txt
    ```

    - #### Windows
    ```
        ./path/to/venv/bin/activate
        pip install -r requirements\dev.<os-platform>.txt
    ```

3. Launch the service
```
    uvicorn main:app --workers 1 --host 0.0.0.0 --port 8008
```

## Posting requests locally
When the service is running, try this link in your browser
```
    127.0.0.1:8008/docs
```

You can test the project with pytest by running the command 
```
    pytest
```


# Refrences
1. deploy_DL_project Repository. [link](https://github.com/Semicolon-Tech/deploy_DL_project_with_fastapi)
2. FastAPI Documentation. [link](https://fastapi.tiangolo.com/)
3. Requests Documentation. [link](https://requests.readthedocs.io/en/master/)
4. Pytest Documentation. [link](https://docs.pytest.org/en/stable/contents.html)
5. Flask Documentation. [link](https://flask.palletsprojects.com/en/1.1.x/)
