from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
from .models import Armor, Weapon, Charm
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
    armors = []
    
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
        "armors": armors,
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
        return JsonResponse({"error": "No weapon type"}, status=400)

    query = json.dumps({"type": weapon_type})
    weapons = fetchAPI(f"weapons?q={query}")

    if not weapons:
        return JsonResponse({"error": "No weapons found"}, status=404)

    return JsonResponse({"weapons": weapons})

def armor_search(request):
    armor_type = request.GET.get("type", "")
    
    if not armor_type:
        return JsonResponse({"error": "No armor type found"}, status=400)

    query = json.dumps({"type": armor_type})
    armors = fetchAPI(f"armor?q={query}")

    if not armors:
        return JsonResponse({"error": "No armor found"}, status=404)

    return JsonResponse({"armors": armors})

def charm_search(request):
    charms = fetchAPI("charms")
    
    return JsonResponse({"charms": charms})

def weapon(weapon_id):
    try:
        weapon = Weapon.objects.get(id=weapon_id)
    except Weapon.DoesNotExist:
        weapon_data = fetchAPI(f"weapons/{weapon_id}")
        
        if not weapon_data or "id" not in weapon_data:  
            return JsonResponse({"error": f"Weapon ID {weapon_id} not found in API"}, status=404)

        weapon = Weapon.objects.create(
            id = castToInt(weapon_data["id"]),
            type = str(weapon_data["type"]),
            rarity = castToInt(weapon_data["rarity"]),
            attack = weapon_data.get("attack", {}),
            elderseal = str(weapon_data["elderseal"]) if "elderseal" in weapon_data else None,
            attributes = weapon_data.get("attributes", {}),
            damageType = str(weapon_data["damageType"]),
            name = str(weapon_data["name"]),
            durability = weapon_data.get("durability", {}),
            slots = weapon_data.get("slots", {}),
            elements = weapon_data.get("elements", {}),
        )
    
    return JsonResponse({
        "id": weapon.id,
        "name": weapon.name,
        "type": weapon.type,
        "rarity": weapon.rarity,
        "attack": weapon.attack.get("display", 0),
        "attributes": weapon.attributes,
        "elderseal": weapon.elderseal,
        "damageType": weapon.damageType
    })

def armor(armor_id):
    try:
        armor = Armor.objects.get(id=armor_id)
    except Armor.DoesNotExist:
        armor_data = fetchAPI(f"armor/{armor_id}")
        
        if not armor_data or "id" not in armor_data:  
            return JsonResponse({"error": f"Armor ID {armor_id} not found in API"}, status=404)

        armor = Armor.objects.create(
            id = castToInt(armor_data["id"]),
            type = str(armor_data["type"]),
            rank = str(armor_data["rank"]),
            rarity = castToInt(armor_data["rarity"]),
            defense = armor_data.get("defense", {}),
            resistances = armor_data.get("resistances", {}),
            name = str(armor_data["name"]),
            slots = armor_data.get("slots", {}),
            skills = armor_data.get("skills", {}),
        )

    return JsonResponse({
        "id": armor.id,
        "name": armor.name,
        "type": armor.type,
        "rarity": armor.rarity,
        "defense": armor.defense.get("base", 0),
        "resistances": armor.resistances
    })
    
def charm(charm_id):
    try:
        charm = Charm.objects.get(id=charm_id)
    except Charm.DoesNotExist:
        charm_data = fetchAPI(f"charm/{charm_id}")
        
        if not charm_data or "id" not in charm_data:  
            return JsonResponse({"error": f"Charm ID {charm_id} not found in API"}, status=404)

        charm = Charm.objects.create(
            id = castToInt(charm_data["id"]),
            name = str(charm_data["name"]),
            ranks = charm_data.get("ranks", {}),
        )

    return JsonResponse({
        "id": charm.id,
        "name": charm.name,
        "ranks": charm.ranks,
    })
    
    
    
    
    
def weapon_list(request):
    weapons = fetchAPI("weapons")
    
    return render(request, "pages/buildMaker.html", {"weapons": weapons})

def armor_list(request):
    armors = fetchAPI("armor")

    return render(request, "pages/buildMaker.html", {"armors": armors})