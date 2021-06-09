#!/usr/bin/env python3
# Imports
import re

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=24)
puzzle_input = puzzle.get_input()

class Army():
    def __init__(
        self, *,
        weaknesses, immunities,
        unit_count, unit_hp,
        attack_dmg, attack_type,
        initiative 
    ):
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.unit_count = unit_count
        self.unit_hp = unit_hp
        self.attack_dmg = attack_dmg
        self.attack_type = attack_type
        self.initiative = initiative
    
    def effective_power(self):
        return self.attack_dmg * self.unit_count

    def choose_target(self, enemies):
        damage_would_deal = float("-inf")
        chosen_enemy = None
        for enemy in enemies:
            damage_to_deal = self.effective_power()
            if self.attack_type in enemy.immunities:
                damage_to_deal = 0
            elif self.attack_type in enemy.weaknesses:
                damage_to_deal *= 2
            if damage_to_deal > damage_would_deal:
                damage_would_deal = damage_to_deal
                chosen_enemy = enemy
            elif damage_to_deal == damage_would_deal:
                chosen_enemy = max(
                    reversed(sorted([enemy, chosen_enemy], key=lambda e: e.initiative)),
                    key=lambda e: e.effective_power()
                )

        return chosen_enemy

    def take_attack(self, attacking_army):
        damage_to_deal = attacking_army.effective_power()
        if attacking_army.attack_type in self.immunities:
            return True
        elif attacking_army.attack_type in self.weaknesses:
            damage_to_deal *= 2
        units_lost = min(damage_to_deal // self.unit_hp, self.unit_count)
        self.unit_count -= units_lost
        return self.unit_count > 0

    def attack(self, chosen_target):
        if chosen_target:
            return chosen_target.take_attack(self)
        return False

    def __repr__(self):
        return f"Army(units={self.unit_count}, weaknesses={self.weaknesses}, immunities={self.immunities}, attack_dmg={self.attack_dmg}, attack_type={self.attack_type}, initiative={self.initiative})"

class ReindeerBody():
    ARMY_LINE = re.compile(r"(\d+) units each with (\d+) hit points"
    "(?: "
    "\((?:;*\s*(immune to (?:\s*\w+\s*,*)*)|;*\s*(weak to (?:\s*\w+\s*,*)*))*\)"
    ")?"
    " with an attack that does (\d+) (\w+) damage"
    " at initiative (\d+)")

    @staticmethod
    def parse_army(army_line):
        matches = ReindeerBody.ARMY_LINE.match(army_line)
        army_info = dict()
        info = list(matches.groups())
        to_immunity_list = lambda m: \
            set(map(lambda i: i.strip(), m[len("immune to "):].split(",")))
        to_weakness_list = lambda m: \
            set(map(lambda i: i.strip(), m[len("weak to "):].split(",")))
        army_info["unit_count"] = int(matches.group(1))
        army_info["unit_hp"] = int(matches.group(2))
        army_info["immunities"] = to_immunity_list(matches.group(3)) if matches.group(3) is not None else set()
        army_info["weaknesses"] = to_weakness_list(matches.group(4)) if matches.group(4) is not None else set()
        army_info["attack_dmg"] = int(matches.group(5))
        army_info["attack_type"] = matches.group(6)
        army_info["initiative"] = int(matches.group(7))
        return Army(**army_info)

    @staticmethod
    def parse(puzzle_input):
        immune_system = []
        infection = []
        searching_for = None
        for line in puzzle_input:
            if not line:
                continue
            
            if line.startswith("Immune System"):
                searching_for = "Immune System"
            elif line.startswith("Infection"):
                searching_for = "Infection"
            else:
                army = ReindeerBody.parse_army(line)
                if searching_for == "Immune System":
                    immune_system.append(army)
                elif searching_for == "Infection":
                    infection.append(army)
        
        return immune_system, infection



# Actual Code
immune_system,infection = ReindeerBody.parse(puzzle_input)

while immune_system and infection:
    # target selection:
    immune_system_targets = {}
    infection_targets = {}
    # Choose targets
    selection_immune_system = list(immune_system)
    immune_system.sort(key=lambda a: a.initiative, reverse=True)
    immune_system.sort(key=lambda a: a.effective_power(), reverse=True)
    
    selection_infection = list(infection)
    infection.sort(key=lambda a: a.initiative, reverse=True)
    infection.sort(key=lambda a: a.effective_power(), reverse=True)
    
    
    for army in immune_system:
        immune_system_targets[army] = army.choose_target(selection_infection)
        if immune_system_targets[army]:
            selection_infection.remove(immune_system_targets[army])
    
    for army in infection:
        infection_targets[army] = army.choose_target(selection_immune_system)
        if infection_targets[army]:
            selection_immune_system.remove(infection_targets[army])

    # Perform  Attacks
    for army in reversed(sorted(immune_system + infection, key=lambda a: a.initiative)):
        if army.unit_count == 0:
            continue
        if army in immune_system:
            army.attack(immune_system_targets[army])
        if army in infection:
            army.attack(infection_targets[army])
    
    # Delete killed groups
    immune_system = list(filter(lambda a: a.unit_count, immune_system))
    infection = list(filter(lambda a: a.unit_count, infection))
    # for army in immune_system + infection:
    #     print(army)
    # print("====")
# Result

print(sum(
    army.unit_count
    for army in immune_system + infection
))