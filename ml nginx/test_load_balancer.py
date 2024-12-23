import requests
import time

def test_load_balancing():
    url = "http://localhost/health"
    
    print("Testing load balancing with 10 requests...")
    for i in range(10):
        response = requests.get(url)
        print(f"Request {i+1}: Container ID = {response.json()['container_id']}")
        time.sleep(0.5)

if __name__ == "__main__":
    test_load_balancing() 