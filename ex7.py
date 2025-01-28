import csv

# Global BST root
ownerRoot = None

# 'defines' for getting rid of magic numbers

# Main menu options
MAIN_NEW_POKEDEX = 1
MAIN_EXIST_POKEDEX = 2
MAIN_DELETE_POKEDEX = 3
MAIN_SORT_OWNERS = 4
MAIN_PRINT_ALL = 5
MAIN_EXIT = 6

# owner sub-menu options
OWNER_ADD_POKEMON = 1
OWNER_DISPLAY_POKEDEX = 2
OWNER_RELEASE_POKEMON = 3
OWNER_EVOLVE_POKEMON = 4
OWNER_BACK = 5

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    # negative bool to accoutn for negative inputs
    negative = False
    # take input, and strip whitespace
    usr_input = input(prompt).strip()
    # loop for invalid input / account for negative
    while True:
        # check negative
        if usr_input[0] == "-":
            negative = True
            usr_input = usr_input[1:]

        # chekc if input is digit
        if usr_input.isdigit():
            break

        # if not digit, print invalid input and re-prompt
        print("Invalid input. ()")
        negative = False
        usr_input = input(prompt).strip()

    # convert to int, and return negative if negative
    if negative:
        return int(usr_input) * -1
    return int(usr_input)

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    for pokeDict in HOENN_DATA:
        if pokeDict["ID"] == poke_id:
            return pokeDict
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for pokeDict in HOENN_DATA:
        if pokeDict["Name"] == name:
            return pokeDict
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass


########################
# 2) BST (By Owner Name)
########################

def create_owner_logic():
    """
    Get information from user to create new owner node and insert into BST.
    """

    # set ownerRoot as global ownerRoot for this function
    global ownerRoot
    # first get new owner info:
    new_owner_name = input("Owner name: ")
    # check if owner is already in tree:
    if find_owner_bst(ownerRoot, new_owner_name):
        print(f"Owner '{new_owner_name}' already exists. No new Pokedex created.")
        return
    # next, get starter choice and assign name as string
    print("Choose your starter Pokemon:\n1) Treecko\n2) Torchic\n3) Mudkip")
    starter_choice = read_int_safe("Your choice: ")
    if starter_choice == 1:
        choice_name = "Treecko"
        pass
    elif starter_choice == 2:
        choice_name = "Torchic"
        pass
    elif starter_choice == 3:
        choice_name = "Mudkip"
        pass
    else:
        # edge case: invalid choice number, return without creating new owner
        print("Invalid. No new Pokedex created.")
        return
    # create the node
    owner_node = create_owner_node(new_owner_name, get_poke_dict_by_name(choice_name))
    # insert new owner node into BST
    ownerRoot = insert_owner_bst(ownerRoot, owner_node)
    # print success message
    print(f"New Pokedex created for {new_owner_name} with starter {choice_name}.")


def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    # create dict (BST node) with owner name, pokedex, and left/right as None
    ownerDict = {'owner': owner_name, 
                 'pokedex': [first_pokemon],
                 'left': None,
                 'right': None}
    return ownerDict

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """

    # first, if root is empty, insert node here
    if root == None:
        return new_node
    # next, if new node's owner name is less than root's owner name, insert left
    if new_node['owner'] < root['owner']:
        root['left'] = insert_owner_bst(root['left'], new_node)
        pass
    # if new node's owner name is greater than root's owner name, insert right
    elif new_node['owner'] > root['owner']:
        root['right'] = insert_owner_bst(root['right'], new_node)
        pass
    # now that we've inserted, return the root
    return root
    

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    # must check both sides, as because of capital letters, we don't necessarily know bigger or smaller
    # if root is empty, return None
    if root == None:
        return None
    # if owner name is the same as root's owner name, return root
    if owner_name.lower() == root['owner'].lower():
        return root
    # check BOTH sides to account for edge case in capital letters
    # get left side recursive, if exists, ie not None, return it
    leftSide = find_owner_bst(root['left'], owner_name)
    if leftSide:
        return leftSide
    # get right side recursive, if exists, ie not None, return it
    rightSide = find_owner_bst(root['right'], owner_name)
    if rightSide:
        return rightSide
    # if here, then no owner found, return None
    return None

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    pass


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    # first, get the ID of the Pokemon to add
    IDChoice = read_int_safe("Enter Pokemon ID to add: ")
    # next, get the Pokemon dict by ID
    pokemonToAdd = get_poke_dict_by_id(IDChoice)
    # if the Pokemon is not found, print message and return
    if not pokemonToAdd:
        print(f"ID {IDChoice} not found in Honen data.")
        return
    # if the Pokemon is already in the pokedex, print message and return
    if pokemonToAdd in owner_node['pokedex']:
        print(f"Pokemon already in the list. No changes made.")
        return
    # if the Pokemon is not in the pokedex, add it and print success message
    owner_node['pokedex'].append(pokemonToAdd)
    print(f"Pokemon {pokemonToAdd['Name']} (ID {pokemonToAdd['ID']}) added to {owner_node['owner']}'s Pokedex.")


def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    pass

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    pass


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """

    # set ownerRoot as global ownerRoot for this function
    global ownerRoot

    if not ownerRoot:
        print("No owners at all.")
        return

    # get owner name
    owner_name = input("Owner name: ")
    # find owner node
    owner_node = find_owner_bst(ownerRoot, owner_name)
    # if owner node not found, print message and return
    if not owner_node:
        print(f"Owner '{owner_name}' not found.")
        return
    # if owner node found, print menu and get choices
    while True:
        print(f"\n-- {owner_node['owner']}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")
        choice = read_int_safe("Your choice: ")
        # TODO: UP TO HERE IN LOGIC
        if choice == OWNER_ADD_POKEMON:
            add_pokemon_to_owner(owner_node)
            pass
        elif choice == OWNER_DISPLAY_POKEDEX:
            # display_filter_sub_menu(owner_node)
            pass
        elif choice == OWNER_RELEASE_POKEMON:
            # release_pokemon_by_name(owner_node)
            pass
        elif choice == OWNER_EVOLVE_POKEMON:
            # evolve_pokemon_by_name(owner_node)
            pass
        elif choice == OWNER_BACK:
            return
        else:
            print("Invalid choice.")


def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """

    while True:
        # print main menu options
        print("\n=== Main Menu ===")
        print("1. New Pokedex")
        print("2. Existing Pokedex")
        print("3. Delete a Pokedex")
        print("4. Sort owners")
        print("5. Print all")
        print("6. Exit")

        # get choice and check which option that is
        choice = read_int_safe("Your choice: ")
        if choice == MAIN_NEW_POKEDEX:
            create_owner_logic()
            pass
        elif choice == MAIN_EXIST_POKEDEX:
            existing_pokedex()
            pass
        elif choice == MAIN_DELETE_POKEDEX:
            pass
        elif choice == MAIN_SORT_OWNERS:
            pass
        elif choice == MAIN_PRINT_ALL:
            pass
        elif choice == MAIN_EXIT:
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")

def main():
    """
    Entry point: calls main_menu().
    """
    main_menu()

if __name__ == "__main__":
    main()
