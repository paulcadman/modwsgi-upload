# vim: set filetype=python:

def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        output = environ['wsgi.input'].read()
        contentType = environ['CONTENT_TYPE']
    else:
        output = "Server running"
        contentType = 'text/plain'

    if not output:
        output = "something went wrong"
        status = '500 Internal Error'
    else:
        status = '200 OK'

    response_headers = [('Content-type', contentType),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
