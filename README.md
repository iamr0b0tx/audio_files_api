# audio_files_api
CRUD Backend for Audio Files

## Project setup
Before going through the steps make sure you have the following pre-installed

### Tools and Resources
1. Python 3.6+
2. Virtualenv
3. Postgresql 
    1. Download the application [link](). 
    2. Install Postgresql and set up root (posgres)
    3. Set up two databases namely __audio_file_db__ and __audio_file_test_db__.
    

Make sure to download/clone this repository and navigate to the folder in your terminal. Now follow the indtructions below

1. Create the virtual environment.
```
    virtualenv /path/to/venv --python=/path/to/python3
```
You can find out the path to your `python3` interpreter with the command `which python3`.

2. Activate the environment and install dependencies. `<os-platform>` is a placeholder for windows/linux.
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

You can test the project with pytest by running the command. You can check Github Actions for the status of tests [here](https://github.com/iamr0b0tx/audio_files_api/actions) 
```
    pytest
```


# Refrences
1. deploy_DL_project Repository. [link](https://github.com/Semicolon-Tech/deploy_DL_project_with_fastapi)
2. FastAPI Documentation. [link](https://fastapi.tiangolo.com/)
3. Requests Documentation. [link](https://requests.readthedocs.io/en/master/)
4. Pytest Documentation. [link](https://docs.pytest.org/en/stable/contents.html)
5. Flask Documentation. [link](https://flask.palletsprojects.com/en/1.1.x/)
