"""
    File to be exectuted by Cloud Function.
"""


def main(request):
    """
        Entry point - Do not change name of this function.
    """
    # return ("Hello from Jonny, Yi and Andreas")
    request_json = request.get_json(silent=True)
    request_args = request.args

    # if request_json and 'name' in request_json:
    #     name = request_json['name']
    # elif request_args and 'name' in request_args:
    #     name = request_args['name']
    # else:
    #     name = 'World'
    # return 'Hello {}!'.format(escape(name))
    print(request_json)
    print(type(request_json))
    
    print(request_args)
    print(type(request_args))

    return (request_json)