# test_connection.py
import requests
from config import GEMINI_API_KEY

print("Testing connection to Gemini API...")
print(f"API Key: {GEMINI_API_KEY[:10]}...")

try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    response = requests.get(url, timeout=30)
    print(f"✅ Connection successful! Status: {response.status_code}")
    print(f"Available models: {len(response.json().get('models', []))}")
except requests.exceptions.ConnectTimeout:
    print("❌ Connection timeout - Cannot reach Google servers")
    print("Possible causes:")
    print("1. Firewall blocking googleapis.com")
    print("2. VPN/Proxy interference")
    print("3. DNS issues")
except Exception as e:
    print(f"❌ Error: {str(e)}")
