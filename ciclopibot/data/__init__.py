"""This folder contains user data.

Therefore, it must be .gitignored and excluded from python packaging.

Examples of data files
- `ciclopi.db`: bot SQLite database file
- Info and erro logs
- `config.py`: configuration file providing local host and port where web app
    should run
    ```python
    local_host = '127.0.0.1'
    port = 8080
    ```
- `passwords.py`: secret file where you can store your bot token
    ```python
    bot_token = "111222333:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    ```
"""
