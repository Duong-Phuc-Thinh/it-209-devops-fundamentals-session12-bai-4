import sys
import requests

def check_vps_health(vps_ip, port=8080):
    url = f"http://{vps_ip}:{port}/actuator/health"
    print(f"Dang kiem tra health check tai: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        if response.status_code == 200:
            print("SUCCESS: Ung dung da khoi chay va hoat dong binh thuong!")
            return True
        else:
            print("FAILURE: Ung dung tra ve ma loi nguyen nhan khac 200.")
            return False
    except Exception as e:
        print(f"ERROR: Khong the ket noi toi VPS ({e})")
        return False

if __name__ == "__main__":
    vps_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    check_vps_health(vps_ip)
