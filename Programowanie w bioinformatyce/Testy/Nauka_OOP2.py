# from random import choice

# class Monster:
#     def __init__(self,func):
#         self.func = func
        
# class Attacks:   
#     def bite(self):
#         print('I bite')
        
#     def strike(self):
#         print('I strike')
        
#     def slash(self):
#         print('I slash')
        
#     def kick(self):
#         print('I kick')


# method = choice(['bite','strike','slash','kick'])
# monster = Monster(getattr(Attacks(), method))

# monster.func()




class Monster:
    def __init__(self,health,energy,**kwargs):
        # kwargs to każdy kolejny argument trzymany
        # w kolejnych słownikach do multiple inheritance
        self.health = health
        self.energy = energy
        print(f'Monster attributes:\
              \nhealth: {health}\
              \nenergy: {energy}\n')
        # super().__init__(**kwargs) # Wie, które kolejne wybrać do inheritance
        
    def update_energy(self,amount):
        self.energy += amount

    def get_damage(self,amount):
        self.health -= amount
        print(f'Monster got damage: {amount}\
              \nhealth: {self.health}\
              \nenergy: {self.energy}\n')


class Hero:
    def __init__(self,damage,monster,**kwargs):
        self.damage = damage
        self.monster = monster
        print(f"Hero's damage: {damage}\n")
        # super().__init__()
        
    def attack(self):
        self.monster.get_damage(self.damage)


class Shark(Monster,Hero):
    def __init__(self,bite_strength,health,energy):
        self.bite_strength = bite_strength
        # super().__init__(health=health, energy=energy)

monster1 = Monster(health = 100, energy = 50)
hero = Hero(damage = 30, monster = monster1)

hero.attack()
hero.attack()

# shark = Shark(
    # bite_strength=50,
    # health=200,
    # energy=55)

# print(shark.health)