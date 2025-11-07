class Monster:
    '''A monster that has some attributes'''
    def __init__(self,health,energy):
        self.health = health
        self.energy = energy
        print(f'\nMonster attributes:\
              \nhealth: {health}\
              \nenergy: {energy}')
    
        # Prytawne atrybuty
        self._id = 5 # Tylko konwencja ale stwierdza się
                     # Żeby tego nie ruszać!
    
    # Metody
    def attack(self,amount):
        print('The monster attacked!')
        print(f'{amount} of damage was dealt')
        self.energy -= 20
        print(f'energy remained {self.energy}')
    
    def move(self,speed):
        print("The monster has moved")
        print(f'monster speed is {speed}')
        
monster1 = Monster(20,10)

# hasattr oraz settr
if hasattr(monster1, 'health'):
    print(f'Monster has {monster1.health} health')
    
# setattr ustawia atrybuty dodatkowo
# TO SAMO: monster1.weapon = 'sword'
# Ale efektywnie dodaje nowe atrybuty

# setattr(monster1, 'weapon', 'sword')
# print(monster1.weapon)

new_attributes = (['Weapon','axe'],
                  ['Armor','shield'],
                  ['Potion','mana'])
for attr,value in new_attributes:
    setattr(monster1,attr,value)
    
print(vars(monster1)) # Pokazuje atrybuty monstera

# doc
print(monster1.__doc__)