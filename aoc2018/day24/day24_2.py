#!/usr/bin/env python3
# Imports
import re

from copy import deepcopy
from collections import defaultdict
from math import ceil

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=24)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "Immune System:",
#     "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2",
#     "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3",
#     "Infection:",
#     "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1",
#     "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4",
# ]
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

        #dmg/unit recieved from each source
        self.dmg_recieved = 0
        self.boost = 0
    
    def effective_power(self):
        return (self.attack_dmg + self.boost) * self.unit_count

    def choose_target(self, enemies):
        damage_would_deal = 0
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
            elif damage_to_deal == damage_would_deal and damage_to_deal > 0:
                if enemy.effective_power() != chosen_enemy.effective_power():
                    chosen_enemy = max([enemy, chosen_enemy], key=lambda e: e.effective_power())
                else:
                    chosen_enemy = max([enemy, chosen_enemy], key=lambda e: e.initiative)

        return chosen_enemy

    def take_attack(self, attacking_army):
        damage_to_deal = attacking_army.effective_power()
        if attacking_army.attack_type in self.immunities:
            return True
        elif attacking_army.attack_type in self.weaknesses:
            damage_to_deal *= 2
        units_lost = min(damage_to_deal // self.unit_hp, self.unit_count)
        self.dmg_recieved += attacking_army.unit_count * (2 if attacking_army.attack_type in self.weaknesses else 1)
        self.unit_count -= units_lost
        return self.unit_count > 0

    def attack(self, chosen_target):
        if chosen_target:
            return chosen_target.take_attack(self)
        return False

    def __repr__(self):
        # return f"Army(units={self.unit_count}, weaknesses={self.weaknesses}, immunities={self.immunities}, attack_dmg={self.attack_dmg}, attack_type={self.attack_type}, initiative={self.initiative})"
        return f"Army(units={self.unit_count})"

class ReindeerBody():
    ARMY_LINE = re.compile(r"(\d+) units each with (\d+) hit points"
    "(?: "
    "\((?:;*\s*(immune to (?:\s*\w+\s*,*)*)|;*\s*(weak to (?:\s*\w+\s*,*)*))*\)"
    ")?"
    " with an attack that does (\d+) (\w+) damage"
    " at initiative (\d+)")

    def __init__(self, immune_system, infection):
        self.immune_system = immune_system
        self.infection = infection
    
    def simulate_battle(self):
        surviving_immune_system, surviving_infection = list(), list()

        min_score = None
        while not surviving_immune_system:
            print("BOOSTED BY", self.immune_system[0].boost, min_score)
            for army in self.immune_system:
                army.boost += 100
            
            immune_system = deepcopy(self.immune_system)
            infection = deepcopy(self.infection)
            surviving_immune_system, surviving_infection =  ReindeerBody.do_battle(immune_system, infection)
        while surviving_immune_system:
            print("BOOSTED BY", self.immune_system[0].boost, min_score)
            min_score = sum(army.unit_count for army in surviving_immune_system)
            for army in self.immune_system:
                army.boost -= 1
            
            immune_system = deepcopy(self.immune_system)
            infection = deepcopy(self.infection)
            surviving_immune_system, surviving_infection =  ReindeerBody.do_battle(immune_system, infection)
        return min_score

    @staticmethod
    def do_battle(immune_system, infection):
        while immune_system and infection:
            print("BATTLING", len(immune_system), len(infection), end="\r")
            # target selection:
            targets = {}
            # Choose targets
            selection_immune_system = list(immune_system)
            immune_system.sort(key=lambda a: a.initiative, reverse=True)
            immune_system.sort(key=lambda a: a.effective_power(), reverse=True)
            
            selection_infection = list(infection)
            infection.sort(key=lambda a: a.initiative, reverse=True)
            infection.sort(key=lambda a: a.effective_power(), reverse=True)
            
            for army in immune_system:
                targets[army] = army.choose_target(selection_infection)
                if targets[army]:
                    selection_infection.remove(targets[army])
            
            for army in infection:
                targets[army] = army.choose_target(selection_immune_system)
                if targets[army]:
                    selection_immune_system.remove(targets[army])

            # Perform  Attacks
            any_did_dmg = False
            for army in reversed(sorted(immune_system + infection, key=lambda a: a.initiative)):
                if army.unit_count == 0 or not targets[army]:
                    continue
                original_unit_count = targets[army].unit_count
                army.attack(targets[army])
                any_did_dmg = any_did_dmg or targets[army].unit_count != original_unit_count
            
            # Delete killed groups
            immune_system = list(filter(lambda a: a.unit_count, immune_system))
            infection = list(filter(lambda a: a.unit_count, infection))
            if infection and immune_system and not any_did_dmg:
                for army in targets:
                    if not targets[army]:
                        print(f"{army}({army.effective_power()}, {army.attack_type}) => {None}")
                    else:
                        print(f"{army}({army.effective_power()}, {army.attack_type}) => {targets[army]}({targets[army].unit_hp},{targets[army].immunities},{targets[army].weaknesses})")
                        army.attack(targets[army])
                        print(f"{targets[army]}")
                raise ValueError(f"Will Infinite Loop! {len(infection)}, {len(immune_system)}, {targets}")
        return immune_system, infection

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
        
        return ReindeerBody(immune_system, infection)

# Actual Code
rudolf = ReindeerBody.parse(puzzle_input)
# immune_system, infection, original_armies =  rudolf.simulate_battle()
# for army in immune_system + infection:
#     print(army.dmg_recieved)
    # print("====")

# Result
print(rudolf.simulate_battle(), " "*30)
# for army in rudolf.immune_system:
#     army.boost = 72
# immune_system = deepcopy(rudolf.immune_system)
# infection = deepcopy(rudolf.infection)
# surviving_immune_system, surviving_infection =  ReindeerBody.do_battle(immune_system, infection)
# print(surviving_immune_system, surviving_infection)