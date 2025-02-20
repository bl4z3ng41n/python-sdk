from anon_python_sdk import Anon


anon = Anon()

try:
    anon.start_vpn("de")
    resp = anon.socks.get("http://ip-api.com/json")
    print(resp.text)
finally:
    anon.stop_vpn()
