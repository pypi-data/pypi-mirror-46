# Code Examples

The Python Downloader has two architectural pieces. The first are a
set of methods to manipulate metadata about files and generate a
Cartd friendly metadata document. The second is a set of methods to
interact with the Cartd service to wait and download the files.

## Download Transaction Info

The download setup described below creates a temporary directory to
download the data to.

```python
from tempfile import mkdtemp

down_path = mkdtemp()
down = Downloader(cart_api_url='http://127.0.0.1:8081')
resp = requests.get('http://127.0.0.1:8181/status/transactions/by_id/67')
assert resp.status_code == 200
down.transactioninfo(down_path, resp.json())
```

## Download Cloud Event

Often CloudEvents are handled in web server frameworks. Here's an
example of using the downloader in [CherryPy](https://cherrypy.org/).
This example can be launched as a consumer of CloudEvents sent by
the [Pacifica Notifications](https://pacifica-notifications.readthedocs.io)
service.

```python
from tempfile import mkdtemp
import cherrypy

class Root(object):
    exposed = True
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        """Accept the cloud event data and return the local download path."""
        down_path = mkdtemp()
        down = Downloader(cart_api_url='http://127.0.0.1:8081')
        down.cloudevent(down_path, cherrpy.request.json)
        return { 'download_path': down_path }


cherrypy.quickstart(Root(), '/', {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }
})
```
