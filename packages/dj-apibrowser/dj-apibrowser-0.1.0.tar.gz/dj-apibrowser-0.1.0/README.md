# Generic GUI for any RESTful API

See the demo at <https://apibrowser-demo.herokuapp.com/> ([source](https://gitlab.com/lew21/demoapi)).

`dj-apibrowser` itself is just a trivial middleware that serves [APIBrowser](https://gitlab.com/lew21/apibrowser), which is written in JS, and works purely in the web browser. It returns the APIBrowser HTML code whenever a web browser navigates to a page.

## Installation
```sh
pip install dj-apibrowser
```

### settings.py
* Add `dj_apibrowser.APIBrowserServerMiddleware` to the list of `MIDDLEWARE`s.
* If neccesary, specify on which endpoints should we serve APIBrowser. Default config means that this is disabled on paths starting from /admin/, and enabled on all other paths:
```
API_ENDPOINTS = [
    ('admin/', False),
    ('', True),
]
```
