from django.db import models

# Create your models here.


#armor Section
class Armor(models.Model):
    id = models.IntegerField(primary_key = True)
    type = models.CharField(max_length = 50, default = '')
    rank = models.CharField(max_length = 50, default = '')
    rarity = models.IntegerField(default = 0)
    defense = models.JSONField(default=dict)
    resistances = models.JSONField(default=dict)
    #attributes - not needed
    name = models.CharField(max_length = 50, default = '')
    slots = models.JSONField(default=dict)
    skills  = models.JSONField(default=dict)
    #armorSet set bonus are going to have to be looked up in armor/sets matching bonus id
    #pieces is the min requirment
    def __str__(self):
        return f"id: {self.id}"
    
#armor Sectoin Ends

#weapons Section
class Weapon(models.Model):
    id = models.IntegerField(primary_key = True)
    type = models.CharField(max_length = 50, default = '')
    rarity = models.IntegerField(default = 0)
    attack = models.JSONField(default=dict)
    elderseal = models.CharField(max_length = 50, default = '')
    attributes = models.JSONField(default=dict)
    damageType = models.CharField(max_length = 50, default = '')
    name = models.CharField(max_length = 50, default = '')
    durability = models.JSONField(default=dict, null=True, blank=True)
    slots = models.JSONField(default=dict)
    elements = models.JSONField(default=dict)
    def __str__(self):
        return f"id: {self.id}"

