from API.API import app
from API.sqlite import Sqlite

if __name__ == '__main__':
    sqlite = Sqlite('./example.db')
    app.run()
