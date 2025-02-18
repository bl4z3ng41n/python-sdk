from anon_python_sdk import Socks, Config, Process


# Create a configuration
config = Config(
    auto_terms_agreement=True,
    display_log=False,
    exit_countries=["DE"],
)

# Initialize and start the runner
anon = Process.launch_anon(anonrc_path=config.to_file())

socks = Socks()

try:
    # Example GET request
    response = socks.get("https://check.en.anyone.tech/api/ip")
    print("GET Response:")
    print(response.text)

    # Example POST request
    post_url = "https://httpbin.org/post"
    post_data = {"key": "value"}
    response = socks.post(post_url, json=post_data)
    print("POST Response:")
    print(response.json())

    # Example DELETE request
    response = socks.delete("https://httpbin.org/delete")
    print("DELETE Response:")
    print(response.json())

except RuntimeError as e:
    print(f"Request error: {e}")

finally:
    anon.stop()
