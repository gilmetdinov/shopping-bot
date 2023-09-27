def check_mass_send_response(response: dict):
    if len(response['success']) == 0:
        return {'status': 'error',
                'message': "Couldn't send the message to any of chat ids!"}
    elif len(response['fail']) == 0:
        return {'status': 'success'}
    else:
        return {'status': 'warning',
                'message': "Couldn't send the message to some chat ids!",
                'failed': response['fail']}
