from abc import ABC, abstractmethod


class Material:
    def __init__(self, strength:float):
        self.strength = strength


class Wood(Material):
    def __init__(self, strength:float):
        super().__init__(strength)


class Metal(Material):
    def __init__(self, strength:float, purity:float):
        super().__init__(strength)
        self.purity = purity


class Gemstone(Material):
    def __init__(self, strength:float, magicPower:float):
        super().__init__(strength)
        self.magicPower = magicPower


class Maple(Wood):
    def __init__(self):
        super().__init__(5)


class Ash(Wood):
    def __init__(self):
        super().__init__(3)


class Oak(Wood):
    def __init__(self):
        super().__init__(4)


class Bronze(Metal):
    def __init__(self):
        super().__init__(3, 1.3)


class Iron(Metal):
    def __init__(self):
        super().__init__(6, 1.1)


class Steel(Metal):
    def __init__(self):
        super().__init__(10, 1.8)


class Ruby(Gemstone):
    def __init__(self):
        super().__init__(1, 1.8)


class Sapphire(Gemstone):
    def __init__(self):
        super().__init__(1.2, 1.6)


class Emerald(Gemstone):
    def __init__(self):
        super().__init__(1.6, 1.1)


class Diamond(Gemstone):
    def __init__(self):
        super().__init__(2.1, 2.2)


class Amethyst(Gemstone):
    def __init__(self):
        super().__init__(1.8, 3.2)


class Onyx(Gemstone):
    def __init__(self):
        super().__init__(0.1, 4.6)


class Crafter(ABC):
    @abstractmethod
    def craft(self):
        pass

    @abstractmethod
    def disassemble(self):
        pass


class Weapon:
    def __init__(self, name, primary, secondary):
        self.__name = name
        self.__primary = primary
        self.__secondary= secondary
        self.__damage = 0
        self.__enchanted = False
        self.__enchantment = None 
        self.calculateDamage()

    def getEnchantment(self):
        return self.__enchantment

    def getName(self):
        return self.__name
    
    def getDamage(self):
        return self.__damage
    
    def getPrimary(self):
        return self.__primary
    
    def getSecondary(self):
        return self.__secondary
    
    def getEnchanted(self):
        return self.__enchanted

    def setName(self, name):
        self.__name = name
    
    def setDamage(self, damage):
        self.__damage = damage
    
    def setPrimary(self, primary):
        self.__primary = primary
    
    def setSecondary(self, secondary):
        self.__secondary = secondary
    
    def setEnchanted(self, enchanted):
        self.__enchanted = enchanted

    def setEnchantment(self, enchantment):
        self.__enchantment = enchantment
        self.calculateDamage()

    def calculateDamage(self):
        material1 = self.getPrimary()
        material2 = self.getSecondary()

        if isinstance(self.getPrimary(), Wood) and  isinstance(self.getSecondary(), Wood):
            damage = float(material1.strength*material2.strength)
        
        elif isinstance(self.getPrimary(), Metal) and  isinstance(self.getSecondary(), Metal):
            damage = float((material1.strength*material1.purity)+(material2.strength*material2.purity))

        elif isinstance(self.getPrimary(), Metal) and  isinstance(self.getSecondary(), Wood):
            damage = float(material2.strength*material1.strength*material1.purity)

        if self.getEnchanted():
            enchantment_damage = self.getEnchantment().getMagicDamage()
            damage *= enchantment_damage

        self.setDamage(damage)
            
    def useEffect(self):
        return f"It deals {self.getDamage():.1f} damage."


class Enchantment:
    def __init__(self, name, primaryMaterial, secondaryMaterial):
        self.__name = name
        self.__primaryMaterial = primaryMaterial
        self.__secondaryMaterial = secondaryMaterial
        self.__magicDamage = None
        self.__effect = None
        self.calculateMagicDamage()

    def getName(self):
        return self.__name
    
    def getMagicDamage(self):
        return self.__magicDamage
    
    def getEffect(self):
        return self.__effect
    
    def getPrimary(self):
        return self.__primaryMaterial
    
    def getSecondary(self):
        return self.__secondaryMaterial
    
    def setEffect(self, effect):
        self.__effect = effect

    def setMagicDamage(self, magicDamage):
        self.__magicDamage = magicDamage

    def calculateMagicDamage(self):
        magicDamage = float(self.getPrimary().magicPower + self.getSecondary().magicPower)
        self.setMagicDamage(magicDamage)
    
    def useEffect(self):
        return f"{self.getName()} enchantment and {self.getEffect()}"




class Forge(Crafter):
    def __init__(self):
        self.weapon = None

    def craft(self, weaponName, primaryMaterial:Material, secondaryMaterial:Material, allMaterials):
        self.weapon = Weapon(weaponName, primaryMaterial, secondaryMaterial)
        allMaterials[type(primaryMaterial).__name__] -= 1
        allMaterials[type(secondaryMaterial).__name__] -= 1
        return self.weapon


    def disassemble(self, weapon:Weapon, allMaterials):
        primaryMaterial = weapon.getPrimary()
        secondaryMaterial = weapon.getSecondary()
        allMaterials[type(primaryMaterial).__name__] += 1
        allMaterials[type(secondaryMaterial).__name__] += 1
        return self.weapon


class Enchanter(Crafter):
    def __init__(self):
        self.enchantment = None
        self.recipes = {
            "Holy": "pulses a blinding beam of light",
            "Lava": "melts the armour off an enemy",
            "Pyro": "applies a devastating burning effect",
            "Darkness": "binds the enemy in dark vines",
            "Cursed": "causes the enemy to become crazed",
            "Hydro": "envelops the enemy in a suffocating bubble",
            "Venomous": "afflicts a deadly, fast-acting toxin"
        }

    def craft(self, name, primaryMaterial, secondaryMaterial, allMaterials):
        self.enchantment = Enchantment(name, primaryMaterial, secondaryMaterial)
        allMaterials[type(primaryMaterial).__name__] -= 1
        allMaterials[type(secondaryMaterial).__name__] -= 1
        return self.enchantment

    def disassemble(self, enchantment:Enchantment, allMaterials):
        primaryMaterial = enchantment.getPrimary()
        secondaryMaterial = enchantment.getSecondary()
        allMaterials[type(primaryMaterial).__name__] += 1
        allMaterials[type(secondaryMaterial).__name__] += 1
        return self.enchantment
    
    def enchant(self, weapon:Weapon, enchantedWeapon:str, enchantment:Enchantment):
        weapon.setEnchanted(True)
        weapon.setEnchantment(enchantment)
        enchantment.setEffect(enchantedWeapon)



class Workshop:
    def __init__(self, forge:Forge, enchanter:Enchanter):
        self.forge = forge
        self.enchanter = enchanter
        self.materials = {}
        self.weapons = []
        self.enchantments = []

    def displayWeapons(self):
        retData = ""
        for weapon in self.weapons:
            if weapon.getEnchanted():
                weapon_name = weapon.getEnchantment().getName()
                retData += f"The {weapon.getEnchantment().getEffect()} imbued with a {weapon_name} enchantment and {self.enchanter.recipes[weapon_name]}. {weapon.useEffect()}\n"
            else:
                retData+= f"The {weapon.getName()} in not enchanted. {weapon.useEffect()}\n"
        
        return retData

    def addMaterial(self, materialName, numberOfMaterials):
        self.materials[materialName] = numberOfMaterials

    def displayMaterials(self):
        retData = ""
        for materialName, materialCount in self.materials.items():
            retData += f"{materialName}: {materialCount} remaining.\n"
        return retData
    
    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def removeWeapon(self, weapon):
        self.weapons.remove(weapon)

    def addEnchantment(self, enchantment):
        self.enchantments.append(enchantment)

    def removeEnchantment(self, enchantment):
        self.enchantments.remove(enchantment)

    def displayEnchantments(self):
        retData = ""
        for enchantment in self.enchantments:
            retData += f"A {enchantment.getName()} enchantment is stored in the workshop.\n"
        return retData