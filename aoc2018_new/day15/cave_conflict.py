from collections import defaultdict
from math import inf

class Fighter():
    def __init__(self, row, column):
        self.attack_power = 3
        self.health = 200
        self.position = (row, column)
    
    def attack(self, attackee):
        attackee.health -= self.attack_power

class Elf(Fighter):
    def __str__(self):
        return f"Elf(@{self.position}, health={self.health})"

class Goblin(Fighter):
    def __str__(self):
        return f"Goblin(@{self.position}, health={self.health})"

class Stuck():
    def __init__(self):
        pass

    def __bool__(self):
        return False

class Map():
    dirs = [
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    ]

    def __init__(self):
        self.rounds = 0
        
        self.map = {}
        self.map_size = 0

        self.elves = []
        self.goblins = []
        self.fighters = {}
    
    def set_map(self, initial_map):
        initial_map = list(map(list, initial_map))
        self.map_size = max(len(initial_map), len(initial_map[0]))
        for r, row in enumerate(initial_map):
            for c, item in enumerate(row):
                if item == 'G':
                    self.goblins.append(Goblin(r, c))
                    self.map[(r,c)] = '.'
                elif item == 'E':
                    self.elves.append(Elf(r, c))
                    self.map[(r,c)] = '.'
                else:
                    self.map[(r,c)] = item
        self.fighters = {
            fighter.position: fighter
            for fighter in self.elves + self.goblins
        }
    
    @staticmethod
    def get_enemy_type(fighter_type):
        if fighter_type is Goblin:
            return Elf
        elif fighter_type is Elf:
            return Goblin

    def get_fighter_list(self, fighter_type):
        if fighter_type is Goblin:
            return self.goblins
        elif fighter_type is Elf:
            return self.elves

    def gen_distance_map(self, fighter_type):
        unit_positions = set(f.position for f in self.fighters.values())
        enemy_list = self.get_fighter_list(
            Map.get_enemy_type(fighter_type)
        )
        distance_map = {pos: inf if value == "." else value for pos, value in self.map.items()}
        positions = set((enemy.position, -1) for enemy in enemy_list)
        while positions:
            pos, dist = positions.pop()
            for move_dir in Map.dirs:
                new_pos = (
                    pos[0] + move_dir[0],
                    pos[1] + move_dir[1]
                )
                new_dist = dist + 1
                try:
                    if distance_map[new_pos] == "#" or new_pos in unit_positions:
                        continue
                    elif distance_map[new_pos] > new_dist:
                        distance_map[new_pos] = new_dist
                        positions.add((new_pos, new_dist))
                except Exception as e:
                    print(e)
                    print(new_pos, distance_map[new_pos], fighter_type)
                    raise ValueError()
        return distance_map
    
    def try_attack(self, fighter):
        enemy_type = Map.get_enemy_type(type(fighter))
        to_attack = []
        for attack_dir in Map.dirs:
            attack_pos = (
                fighter.position[0] + attack_dir[0],
                fighter.position[1] + attack_dir[1]
            )
            # if so attack them
            if attack_pos in self.fighters and type(self.fighters[attack_pos]) is enemy_type:
                to_attack.append(self.fighters[attack_pos])
        if to_attack:
            to_attack = min(to_attack, key=lambda f: f.health)
            fighter.attack(to_attack)
            killed = None
            if to_attack.health <= 0:
                killed = to_attack
            return True, killed
        return False, None

    def take_turn(self, fighter, distance_map):
        moved, killed = False, None
        # Check if any adjacent are enemies
        attacked, killed = self.try_attack(fighter)
        if attacked:
            return moved, killed
        # Move to best position
        possible_positions = list()
        for move_dir in Map.dirs:
            move_pos = (
                fighter.position[0] + move_dir[0],
                fighter.position[1] + move_dir[1]
            )
            if type(distance_map[move_pos]) is int:
                possible_positions.append(move_pos)
        if possible_positions:
            del self.fighters[fighter.position]
            fighter.position = min(possible_positions, key=lambda p: distance_map[p])
            try:
                assert(fighter.position not in self.fighters)
            except Exception as e:
                print(distance_map)
                raise e
            self.fighters[fighter.position] = fighter
            moved = True
            # Try attacking again
            attacked, killed = self.try_attack(fighter)
            if attacked:
                return moved, killed
        return moved, killed

    def tick(self):
        distance_maps = {
            fighter_type: self.gen_distance_map(fighter_type)
            for fighter_type in (Goblin, Elf)
        }
        for fighter in sorted(self.fighters.values(), key=lambda f: f.position[0]*self.map_size + f.position[1]):
            if fighter not in self.fighters.values():
                continue
            enemy_list = self.get_fighter_list(Map.get_enemy_type(type(fighter)))
            if not enemy_list:
                return False
            moved, killed = self.take_turn(fighter, distance_maps[type(fighter)])
            if killed:
                del self.fighters[killed.position]
                
                enemy_list.remove(killed)

            if moved or killed:
                distance_maps = {
                    fighter_type: self.gen_distance_map(fighter_type)
                    for fighter_type in (Goblin, Elf)
                }
        self.rounds += 1
        return True
    
    def perform_combat(self, display=False):
        done = False
        while not done:
            done = not self.tick()
            if display:
                print("="*10 + f" {self.rounds} " + "="*10)
                print(self)
        return sum(f.health for f in self.fighters.values()) * self.rounds

    def __str__(self):
        res = ""
        fighter_type_short_name = {
            Elf: "E",
            Goblin: "G",
        }
        for r in range(self.map_size):
            row_exists = False
            for c in range(self.map_size):
                if (r,c) not in self.map:
                    break
                row_exists = True
                res += (
                    self.map[(r, c)] 
                    if (r,c) not in self.fighters else
                    fighter_type_short_name[type(self.fighters[(r,c)])]
                )
            if row_exists:
                for fighter_pos in sorted(self.fighters, key=lambda p: p[1]):
                    if fighter_pos[0] == r:
                        res += (
                            f" {fighter_type_short_name[type(self.fighters[fighter_pos])]}({self.fighters[fighter_pos].health}),"
                        )
                res = res.rstrip(",") + "\n"
        return res

