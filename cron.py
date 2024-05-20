import requests
import time

def keep_alive(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server is alive")
            else:
                print("Server is down")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(500)

if __name__ == '__main__':
    keep_alive('https://updatedflask.onrender.com/healthcheck')
