# from random import randint as rd
class Monster:   
    def __init__(self,health,energy):
        self.health = health
        self.energy = energy
        print(f'\nMonster attributes:\
              \nhealth: {health}\
              \nenergy: {energy}')
                
    def attack(self,amount):
        print('The monster attacked!')
        print(f'{amount} of damage was dealt')
        self.energy -= 20
        print(f'energy remained {self.energy}')
    
    def move(self,speed):
        print("The monster has moved")
        print(f'monster speed is {speed}')


class Shark(Monster):
    def __init__(self,speed,health,energy):
        super().__init__(health,energy)
        self.speed = speed
        print(f'\nShark attributes:\
              \nspeed: {self.speed}\
              \nhealth: {self.health}\
              \nenergy: {self.energy}')
        
    def bite(self):
        print('The shark has bitten')
    
    def move(self):
        print('The shark has moved')
        print(f'The speed of the shark is {self.speed}')
    
class Scorpion(Monster):
    def __init__(self,poison,health,energy):
        super().__init__(health,energy)
        self.poison_damage = poison
    
    def attack(self):
        print('The scorpion has attacked!')
        print(f'it has dealt {self.poison_damage} poison damage')
    
# monster1 = Monster(rd(100,160),rd(20,60))
# monster1 = Monster(health = 100, energy = 60)
shark = Shark(speed = 120, health = 100, energy = 80)
scorpion = Scorpion(health = 60, energy = 50, poison = 10)
