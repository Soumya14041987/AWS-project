import os
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SITE = os.environ.get('site')
EXPECTED = os.environ.get('expected')


def validate(res):
    """Checks whether the EXPECTED string is present in the response content."""
    return EXPECTED in res


def lambda_handler(event, context):
    check_time = event.get('time', str(datetime.utcnow()))
    print(f'Checking {SITE} at {check_time}...')

    try:
        req = Request(SITE, headers={'User-Agent': 'AWS Lambda'})
        with urlopen(req) as response:
            content = response.read().decode('utf-8')  # decode bytes to string
            if not validate(content):
                print('Validation failed: expected content not found.')
                return {
                    'statusCode': 500,
                    'message': 'Validation failed: expected content not found.',
                    'time': check_time
                }
    except HTTPError as e:
        print(f'HTTP error occurred: {e.code} - {e.reason}')
        return {
            'statusCode': e.code,
            'message': f'HTTP error: {e.reason}',
            'time': check_time
        }
    except URLError as e:
        print(f'URL error occurred: {e.reason}')
        return {
            'statusCode': 503,
            'message': f'URL error: {e.reason}',
            'time': check_time
        }
    except Exception as e:
        print(f'Unhandled exception: {str(e)}')
        return {
            'statusCode': 500,
            'message': f'Unhandled exception: {str(e)}',
            'time': check_time
        }
    else:
        print('Validation passed!')
        return {
            'statusCode': 200,
            'message': 'Validation passed!',
            'time': check_time
        }
    finally:
        print('Check complete at {}'.format(str(datetime.now())))
