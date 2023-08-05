# Certificate render
HTML5 + CSS3 template to render a certificate view

Templates rendered with the certificate values will be included in 
``displayHtml`` of certificates so that the certificate can be always 
visualized in the original form.

## Usage
A ``Makefile`` is present to help you developing and using the project

### Run
Use ``make run`` to output a sample certificate renderization

### Serve
Use ``make serve`` to serve the template locally using Python 3 integrated
HTTP server.

> To serve the rendering of an `EDS`, use `make serve-eds`

### Build and upload
Use ``make build`` to create a package distribution and ``make upload`` to 
upload it to PyPi
