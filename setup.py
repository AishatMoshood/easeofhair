'''File starts the server'''
from easetestprojapp import app, manager

if __name__ == '__main__':
    app.run(debug=True)
    manager.run()

    