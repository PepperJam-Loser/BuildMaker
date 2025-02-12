from django.shortcuts import render
import requests
# Create your views here.

def armor(request):
    return render(request, 'pages/armor.html')

def fetchAPI(endpoint, **params):
    targetAPI = "https://mhw-db.com/"
    query = f"{targetAPI}{endpoint}"

    try:
        response = requests.get(query, params=params)
        return response.json()
    except requests.RequestException as e:
        print(f"fetchAPI Error: {e}")
        return None

