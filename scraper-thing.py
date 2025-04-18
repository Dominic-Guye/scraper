import urllib3
import httpx

example_response = httpx.request('get','http://www.example.com')
read_response = example_response.read()
print(read_response)

ortlund = urllib3.request('get','https://truthunites.org')
ortlund_headers = ortlund.headers
ortlund_info = ortlund.info()
ortlund_status = ortlund.status
ortlund_reason = ortlund.reason
ortlund_read = ortlund.data
if len(ortlund_read) > 10:
    print(ortlund_read)
elif len(ortlund_read) in (None,0):
    raise ValueError("The response was null or zero.")
elif ortlund_read != None:
    raise urllib3.exceptions.ResponseError(f"There was a response, but it was way too short. It consisted entirely of {print(ortlund_read)}.")
