# Take-Home Assignment

The repository is a prototype for the CTW take home assignment.

It is implemented by python 3 and integrated with MYSQL db.

## Tech stack

My main language is not python, so all of the libraries and file structure are based on my expereinces on Node.js.

- fastapi: Chose this lib becuase I read the docs and I thought it is easy for integration and good for prototyping.
- uvicorn: A server for running my fastapi services.
- python-dotenv: A library I used to manage my env variables with, can get the env variables by `os.getenv()`.
- pydantic: For request validation. I think the request validation should not be done inside the service, so I prefer to add some kind of middleware in between the service and api controller. Because I had to fulfill the assignment requirement to response the errors ocurred in the correct format, I wrapped the error hanlding for the controller.
- sqlalchemy: ORM for mysql. I prefer using orm more because I can focus more on the logics and they handle most of other stuff for me.
- PyMySQL: for connections to mysql
- cryptography: a runtime dependency for PyMySQL

### development dependencies

Did not appear on the requirements.txt since it is only used in development stage, and would be redundant when creating docker image.

- black: For auto-formatting. I chose black because I googled and found out that only black could make all the quotes double quoted. It was quite annoying to see both in my code when I did not installed it at the begining.

## Getting Started

1. Get an apikey from [AlphaVantage](https://www.alphavantage.co/documentation/)
2. After cloning from this repo, duplicate a `.env.example` and rename it `.env` and put it in the same directory of `.env.example`. Don\'t forget to place your apikey to the field `ALPHAVANTAGE_APIKEY`. For the other fields you may leave it as is.
3. Execute command
   ```
   docker-compose up
   ```
4. From the terminal messages, you may observe that there are some error messages from the app telling that is not able to connect to the db. This is because the mysql server is not allowing connections at that moment. The app will retry until the mysql server is ready for connections.
5. After the following messege appears, the app is ready.
   ```
   INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
   ```
6. An auto generated swagger can be found at `http://localhost:5000/doc`, and you may fire the requests from the GUI.
