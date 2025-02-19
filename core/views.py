from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
from .models import Armor, Weapon
import requests
import json
# Create your views here.

def castToInt(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def buildmaker(request):
    weapons = []
    
    armor_types = {
        "head",
        "chest",
        "gloves",
        "waist",
        "legs",
    }
    
    weapon_types = {
        "great-sword": "GS",
        "long-sword": "LS",
        "sword-and-shield": "SnS",
        "dual-blades": "DB",
        "hammer": "HAM",
        "hunting-horn": "HH",
        "lance": "LAN",
        "gunlance": "GL",
        "switch-axe": "SA",
        "charge-blade": "CB",
        "insect-glaive": "IG",
        "light-bowgun": "LBG",
        "heavy-bowgun": "HBG",
        "bow": "BOW",
    }
    
    context = {
        "weapons": weapons,
        "weapon_types": weapon_types,
        "armor_types": armor_types,
    }

    
    return render(request, "pages/buildMaker.html", context)

def fetchAPI(endpoint, **params):
    targetAPI = "https://mhw-db.com/"
    query = f"{targetAPI}{endpoint}"

    try:
        response = requests.get(query, params=params)
        print(f"API Response ({query}):", response.text)
        return response.json()
    except requests.RequestException as e:
        print(f"fetchAPI Error: {e}")
        return None
    
def weapon_search(request):
    weapon_type = request.GET.get("type", "")
    
    if not weapon_type:
        return JsonResponse({"error": "No weapon type provided"}, status=400)

    query = json.dumps({"type": weapon_type})
    weapons = fetchAPI(f"weapons?q={query}")

    if not weapons:
        return JsonResponse({"error": "No weapons found"}, status=404)

    return JsonResponse({"weapons": weapons})













def armor_list(request):
    armors = fetchAPI("armor")

    if not armors:
        return render(request, "pages/armor.html", {"error": "armor list failure."})

    return render(request, "pages/armor.html", {"armors": armors})

def armor(request, armor_id):
    try:
        armor = Armor.objects.get(id=armor_id)
    except Armor.DoesNotExist:
        armor_data = fetchAPI(f"armor/{armor_id}")
        
        if not armor_data or "id" not in armor_data:  
            return render(request, "pages/armor.html", {"error": f"Armor ID {armor_id} not found in API"})

        armor = Armor.objects.create(
            id = castToInt(armor_data["id"]),
            type = str(armor_data["type"]),
            rank = str(armor_data["rank"]),
            rarity = castToInt(armor_data["rarity"]),
            defense = armor_data.get("defense", {}),
            resistances = armor_data.get("resistances", {}),
            name = str(armor_data["name"]),
            slots = armor_data.get("slots", {}),
            skills = armor_data.get("skills", {})
        )
    return render(request, 'pages/armor.html', {"armor": armor})

def weapon_list(request):
    weapons = fetchAPI("weapons")
    
    return render(request, "pages/buildMaker.html", {"weapons": weapons})

def weapon(request, weapon_id):
    try:
        weapon = Weapon.objects.get(id=weapon_id)
    except Weapon.DoesNotExist:
        weapon_data = fetchAPI(f"weapons/{weapon_id}")
        
        if not weapon_data or "id" not in weapon_data:  
            return render(request, "", {"error": f"Weapon ID {weapon_id} not found in API"})

        weapon = Weapon.objects.create(
            id = castToInt(weapon_data["id"]),
            type = str(weapon_data["type"]),
            rarity = castToInt(weapon_data["rarity"]),
            attack = weapon_data.get("attack", {}),
            elderseal = str(weapon_data["elderseal"]),
            attributes = weapon_data.get("attributes", {}),
            damageType = str(weapon_data["damageType"]),
            name = str(weapon_data["name"]),
            durability = weapon_data.get("durability", {}),
            slots = weapon_data.get("slots", {}),
            elements = weapon_data.get("elements", {}),
        )
    return render(request, '', {"weapon": weapon})