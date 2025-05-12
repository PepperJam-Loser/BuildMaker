from django.shortcuts import render,  get_object_or_404
from django.http import JsonResponse
from .models import Armor, Weapon, Charm, Decoration
import requests
import json
# Create your views here.

def castToInt(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
    
def search(request):

    return render(request, "pages/searchengine.html")

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
    name = request.GET.get("name", "")
    element_type = request.GET.get("element_type", "")
    min_slots = request.GET.get("slots", 0)

    query = {}

    if weapon_type:
        query["type"] = weapon_type

    if name:
        query["name"] = {"$like": f"%{name}%"}

    if element_type:
        query["elements.type"] = element_type
    
    if min_slots:
        query["slots"] = {"$size": int(min_slots)}

    if not query:
        return JsonResponse({"error": "No valid search parameters provided"}, status=400)

    query_string = json.dumps(query)

    weapons = fetchAPI(f"weapons?q={query_string}")

    if not weapons:
        return JsonResponse({"error": "No weapons found"}, status=404)

    return JsonResponse({"weapons": weapons}, status=200)

def armor_search(request):
    armor_types = request.GET.get("type", "")
    name = request.GET.get("name", "")
    min_slots = request.GET.get("slots", 0)
    
    query = {}
    
    if armor_types:
        query["type"] = armor_types

    if name:
        query["name"] = {"$like": f"%{name}%"}
    
    if min_slots:
        query["slots"] = {"$size": int(min_slots)}
        
    query_string = json.dumps(query)

    armors = fetchAPI(f"armor?q={query_string}")

    if not armors:
        return JsonResponse({"error": "No armor found"}, status=404)

    return JsonResponse({"armors": armors}, status=200)

def charm_search(request):
    name = request.GET.get("name", " ")
    
    query = {}
    
    if name:
        query["name"] = {"$like": f"%{name}%"}
        
    query_string = json.dumps(query)
    
    charms = fetchAPI(f"charms?q={query_string}")

    if not charms:
        return JsonResponse({"error": "No charms found"}, status=404)

    return JsonResponse({"charms": charms}, status=200)

def decoration_search(request):
    name = request.GET.get("skills.skillName", " ")
    
    query = {}
    
    if name:
        query["skills.skillName"] = {"$like": f"%{name}%"}
        
    query_string = json.dumps(query)
    
    decorations = fetchAPI(f"decorations?q={query_string}")

    if not decorations:
        return JsonResponse({"error": "No decorations found"}, status=404)

    return JsonResponse({"decorations": decorations}, status=200)

def weapon(request, weapon_id):
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
        "attack": weapon.attack,
        "attributes": weapon.attributes,
        "elderseal": weapon.elderseal,
        "damageType": weapon.damageType,
        "elements" :  weapon.elements,
        "durability" : weapon.durability,
        "slots" : weapon.slots,
    })

def armor(request, armor_id):
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
            slots = armor_data.get("slots", []),
            skills = armor_data.get("skills", []),
            setbonus = armor_data.get("armorSet",{}),
        )

    return JsonResponse({
        "id": armor.id,
        "name": armor.name,
        "type": armor.type,
        "rarity": armor.rarity,
        "defense": armor.defense.get("base", 0),
        "resistances": armor.resistances,
        "slots": armor.slots,
        "skills": armor.skills,
    })
    
def charm(request, charm_id):
    try:
        charm = Charm.objects.get(id=charm_id)
    except Charm.DoesNotExist:
        charm_data = fetchAPI(f"charms/{charm_id}")
        
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
    
def decoration(request, decoration_id):
    try:
        decoration = Decoration.objects.get(id=decoration_id)
    except Decoration.DoesNotExist:
        decoration_data = fetchAPI(f"decorations/{decoration_id}")
        
        if not decoration_data or "id" not in decoration_data:  
            return JsonResponse({"error": f"Decoration ID {decoration_id} not found in API"}, status=404)
    
        decoration = Decoration.objects.create(
            id = castToInt(decoration_data["id"]),
            name = str(decoration_data["name"]),
            skills = decoration_data.get("skills", []),
        )
    return JsonResponse({
        "id": decoration.id,
        "name": decoration.name,
        "skills": decoration.skills,
    })
    
def motion(request):
    weaponType = request.GET.get("weaponType", "")
    
    query = {}
    
    if weaponType:
        query["weaponType"] = {"$like": f"%{weaponType}%"}
        
    query_string = json.dumps(query)
    
    motion = fetchAPI(f"motion-values?q={query_string}")

    if not motion:
        return JsonResponse({"error": "No motion-values found"}, status=404)

    return JsonResponse({"motion": motion}, status=200)

def skills(request):
    skillName = request.GET.get("skillName", "")
    rank = request.GET.get("rank", "")

    try:
        rank_int = int(rank)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid rank"}, status=400)

    if not skillName:
        return JsonResponse({"error": "Missing skill name"}, status=400)

    query = {"name": skillName}
    query_string = json.dumps(query)

    skill_data = fetchAPI(f"skills?q={query_string}")

    if not skill_data:
        return JsonResponse({"error": "Skill not found"}, status=404)

    skill = skill_data[0]
    ranks = skill.get("ranks", [])

    if not ranks:
        return JsonResponse({"error": "No ranks found"}, status=404)
    
    valid_ranks = [r for r in ranks if isinstance(r.get("level"), int)]
    if not valid_ranks:
        return JsonResponse({"error": "No valid rank levels found"}, status=404)

    max_available_level = max(r["level"] for r in valid_ranks)
    chosen_level = min(rank_int, max_available_level)

    best_rank = max(
        (r for r in valid_ranks if r["level"] <= chosen_level),
        key=lambda r: r["level"],
        default=None
    )

    if not best_rank:
        return JsonResponse({"error": "No suitable rank found"}, status=404)

    return JsonResponse({
        "modifiers": best_rank.get("modifiers", {}),
        "rank": best_rank["level"],
        "description": best_rank.get("description", "No description")
    })

def weapon_list(request):
    weapons = fetchAPI("weapons")
    
    return render(request, "pages/buildMaker.html", {"weapons": weapons})

def armor_list(request):
    armors = fetchAPI("armor")

    return render(request, "pages/buildMaker.html", {"armors": armors})