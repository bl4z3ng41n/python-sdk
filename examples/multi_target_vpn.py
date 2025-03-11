from anon_python_sdk import Anon, VPNConfig, VPNRouting


anon = Anon()

try:
    config = VPNConfig(
        routings=[
            VPNRouting("ip-api.com", ["us"]),
            VPNRouting("ipinfo.io", ["de"]),
        ]
    )

    anon.start_vpn_with_config(config)

    # first request
    print("First request")
    resp1 = anon.socks.get("http://ip-api.com/json")
    print(resp1.text)

    # second request
    print("Second request")
    resp2 = anon.socks.get("https://ipinfo.io/json")
    print(resp2.text)
finally:
    anon.stop_vpn()
