#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2018, day=13)
puzzle_input = puzzle.get_input(raw=True)

cart_path = list(map(list, puzzle_input))

row_count, col_count = len(cart_path), len(cart_path[0])
class CartInfo():
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    cart_dir_map = {
        "<": LEFT,
        "^": UP,
        "v": DOWN,
        ">": RIGHT,
    }
    
    CORNERS = set("/\\")
    CROSSROADS = set("+")
    PATHS = set("|-")
    CARTS = set("<>^v")

    dir_cart_map = dict(zip(cart_dir_map.values(), cart_dir_map.keys()))
    @staticmethod
    def cart_to_dir(cart):
        return CartInfo.cart_dir_map[cart]
    
    @staticmethod
    def dir_to_cart(dir):
        return CartInfo.dir_cart_map[dir]

cart_positions = []
for row_index,row in enumerate(cart_path):
    for col_index, item in enumerate(row):
        if item in "><v^":
            cart_positions.append([row_index, col_index, item, "<"])



def move_cart(position):
    row_index, col_index, cart, next_turn = position
    direction = CartInfo.cart_to_dir(cart)
    next_turn = CartInfo.cart_to_dir(next_turn)
    row_index, col_index = (
        row_index + direction[0],
        col_index + direction[1]
    )
    assert(
        0 <= row_index < row_count and 
        0 <= col_index < col_count
    ), f"Invalid index! ({row_index}, {col_index})"
    next_position = cart_path[row_index][col_index]
    if next_position in CartInfo.PATHS | CartInfo.CARTS:
        # just go forward
        position[:2] = row_index, col_index
    
    elif next_position in CartInfo.CROSSROADS:
        if next_turn == CartInfo.UP:
            next_turn = CartInfo.RIGHT
        elif next_turn == CartInfo.LEFT:
            direction = (
                -1 * direction[1],
                direction[0],
            )
            next_turn = CartInfo.UP
        elif next_turn == CartInfo.RIGHT:
            direction = (
                direction[1],
                -1 * direction[0],
            )
            next_turn = CartInfo.LEFT
        cart = CartInfo.dir_to_cart(direction)
        next_turn = CartInfo.dir_to_cart(next_turn)
        position[:] = row_index, col_index, cart, next_turn
    
    elif next_position in CartInfo.CORNERS:
        direction = reversed(direction)
        if next_position == '/':
            direction = tuple(map(lambda d: -d, direction))
        elif next_position == '\\':
            direction = tuple(direction)
        position[:3] = row_index, col_index, CartInfo.dir_to_cart(direction)
    else:
        raise ValueError(str((next_position, (row_index, col_index))))
        # looped back to self
    return

def has_collided(checking_cart):
    for cart in cart_positions:
        if checking_cart is cart:
            continue
        elif cart[:2] == checking_cart[:2]:
            return cart
    return False


# Actual Code
done = False
while not done:
    for cart in sorted(cart_positions, key=lambda c: c[1]*row_count + c[0]):
        move_cart(cart)
        if has_collided(cart):
            row_index, col_index = cart[:2]
            print((col_index,row_index))
            done = True
            break
        # print(">", cart, pos)
    # print()
# Result