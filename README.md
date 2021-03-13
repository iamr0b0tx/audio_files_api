# audio_files_api
CRUD Backend for Audio Files

### Database Specifications
Audio file type can be one of the following:
1. Song
2. Podcast
3. Audiobook

- Song file fields:
    - ID – (mandatory, integer, unique)
    - Name of the song – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)
- Podcast file fields:
    - ID – (mandatory, integer, unique)
    - Name of the podcast – (mandatory, string, cannot be larger than 100
    characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)
    - Host – (mandatory, string, cannot be larger than 100 characters)
    - Participants – (optional, list of strings, each string cannot be larger than
    100 characters, maximum of 10 participants possible)
- Audiobook file fields:
    - ID – (mandatory, integer, unique)
    - Title of the audiobook – (mandatory, string, cannot be larger than 100
    characters)
    - Author of the title (mandatory, string, cannot be larger than 100
    characters)
    - Narrator - (mandatory, string, cannot be larger than 100 characters)
    - Duration in number of seconds – (mandatory, integer, positive)
    - Uploaded time – (mandatory, Datetime, cannot be in the past)


## API specifications
- Create API: The request will have the following fields:
    - audioFileType – mandatory, one of the 3 audio types possible
    - audioFileMetadata – mandatory, dictionary, contains the metadata for one of the three audio files (song, podcast, audiobook)
- Delete API:
    - The route will be in the following format: `<audioFileType>/<audioFileID>`
- Update API:
    - The route be in the following format: `<audioFileType>/<audioFileID>`
    - The request body will be the same as the upload
- Get API:
    - The route `<audioFileType>/<audioFileID>` will return the specific audio
    file
    - The route `<audioFileType>` will return all the audio files of that type

## Project setup
Before going through the steps make sure you have the following pre-installed

### Tools and Resources
1. Python 3.6+
2. Virtualenv
3. Postgresql 
    1. Download the application [link](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads). 
    2. Install Postgresql and set up root (postgres). [link](https://www.postgresqltutorial.com/install-postgresql/)
    3. Set up two databases namely __audio_file__ and __audio_file_test__.
    

Make sure to download/clone this repository and navigate to the folder in your terminal. Now follow the indtructions below

1. Create the virtual environment.
```
    virtualenv /path/to/venv --python=/path/to/python3
```
You can find out the path to your `python3` interpreter with the command `which python3`.

2. Set up `.env` file by duplicating the `.example.env` file(and editing if required).

3. Activate the environment and install dependencies.
    - #### Linux
    ```
        source /path/to/venv/bin/activate
        pip install -r requirements\dev.linux.txt
    ```

    - #### Windows
    ```
        ./path/to/venv/bin/activate
        pip install -r requirements\dev.windows.txt
    ```

4. Launch the service
```
    uvicorn main:app --workers 1 --host 0.0.0.0 --port 8008
```

## Posting requests locally
When the service is running, try this link in your browser/Postman
```
    127.0.0.1:8008
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
