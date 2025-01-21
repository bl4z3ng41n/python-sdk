from anon_python_sdk import SocksClient, AnonConfig, AnonRunner
import time


# Create a configuration
config = AnonConfig(
    auto_terms_agreement=True
)

# Initialize and start the runner
runner = AnonRunner(config)
runner.start()

time.sleep(5)  # Wait for Anon to start

client = SocksClient()

try:
    # Example GET request
    response = client.get("https://check.en.anyone.tech/api/ip")
    print("GET Response:")
    print(response.text)

    # Example POST request
    post_url = "https://httpbin.org/post"
    post_data = {"key": "value"}
    response = client.post(post_url, json=post_data)
    print("POST Response:")
    print(response.json())

    # Example DELETE request
    response = client.delete("https://httpbin.org/delete")
    print("DELETE Response:")
    print(response.json())

except RuntimeError as e:
    print(f"Request error: {e}")

finally:
    runner.stop()
