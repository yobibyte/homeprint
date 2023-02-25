# Client driverless printing.

Have an old printer that is not supported by your current OS? 
Set this flask server on a linux machine, and enjoy printing from your browser.

## How to use

### Server

Start a flask server by `flask run --host=0.0.0.0`. If instead of 0.0.0.0 you put the local ip address of the server, you will be able to print from your smartphone, e.g., `flask run --192.168.1.42:5000`.

### Client

Go to the local server address (e.g. 192.168.1.42:5000) and upload the file.
