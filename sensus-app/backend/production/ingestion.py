def handler(event, context):
    try:
        return response(event, 200)
    except Exception as e:
        return response('Error' + e.message, 400)

def response(message, status_code):
    return message
