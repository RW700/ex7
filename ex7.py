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

# Owner sub-menu options
OWNER_ADD_POKEMON = 1
OWNER_DISPLAY_POKEDEX = 2
OWNER_RELEASE_POKEMON = 3
OWNER_EVOLVE_POKEMON = 4
OWNER_BACK = 5

# Pokedex display menu options
DISP_CERTAIN_TYPE = 1
DISP_EVOLVABLE = 2
DISP_ATTACK_ABOVE = 3
DISP_HP_ABOVE = 4
DISP_NAME_STARTS = 5
DISP_ALL = 6
DISP_BACK = 7

# Print all owners sub-menu options
PRINT_OWNER_BFS = 1
PRINT_OWNER_PRE = 2
PRINT_OWNER_IN = 3
PRINT_OWNER_POST = 4

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
        if usr_input:
            if usr_input[0] == "-":
                negative = True
                usr_input = usr_input[1:]

        # check if input is digit
        if usr_input.isdigit():
            break

        # if not digit, print invalid input and re-prompt
        print("Invalid input.")
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
    for poke_dict in HOENN_DATA:
        if poke_dict["ID"] == poke_id:
            return poke_dict
    return None

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    for poke_dict in HOENN_DATA:
        if poke_dict["Name"] == name:
            return poke_dict
    return None

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    # case for empty list
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return
    
    # print each pokemon in the list in order in format ID, Name, Type, HP, Attack, Can Evolve
    for pokemon in poke_list:
        print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Can Evolve: {pokemon['Can Evolve']}")


def display_certian_type(poke_list):
    """
    Display only Pokemon of a certain type.
    """
    # get type from user
    type_choice = input("Which Type? (e.g. GRASS, WATER): ")
    # create list of Pokemon that match the type (cast to lower so case insensitive)
    type_list = [pokemon for pokemon in poke_list if pokemon['Type'].lower() == type_choice.lower()]
    # display the list
    display_pokemon_list(type_list)

def display_evolvable(poke_list):
    """
    Display only Pokemon that can evolve.
    """
    # create list of Pokemon that can evolve
    evolve_list = [pokemon for pokemon in poke_list if pokemon['Can Evolve'] == "TRUE"]
    # display the list
    display_pokemon_list(evolve_list)

def display_atack_above(poke_list):
    """
    Display only Pokemon with an attack above a certain value.
    """
    # get attack value from user
    attack_choice = read_int_safe("Enter Attack threshold: ")
    # create list of Pokemon with attack above the value
    attack_list = [pokemon for pokemon in poke_list if pokemon['Attack'] > attack_choice]
    # display the list
    display_pokemon_list(attack_list)

def display_hp_above(poke_list):
    """
    Display only Pokemon with HP above a certain value.
    """
    # get HP value from user
    hp_choice = read_int_safe("Enter HP threshold: ")
    # create list of Pokemon with HP above the value
    hp_list = [pokemon for pokemon in poke_list if pokemon['HP'] > hp_choice]
    # display the list
    display_pokemon_list(hp_list)

def display_name_starts(poke_list):
    """
    Display only Pokemon whose name starts with a certain letter(s).
    """
    # get starting letters from user
    name_choice = input("Starting letter(s): ")
    # create list of Pokemon with names starting with the letters
    name_list = [pokemon for pokemon in poke_list if pokemon['Name'].lower().startswith(name_choice.lower())]
    # display the list
    display_pokemon_list(name_list)

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
    owner_dict = {'owner': owner_name, 
                 'pokedex': [first_pokemon],
                 'left': None,
                 'right': None}
    return owner_dict

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
    left_side = find_owner_bst(root['left'], owner_name)
    if left_side:
        return left_side
    # get right side recursive, if exists, ie not None, return it
    right_side = find_owner_bst(root['right'], owner_name)
    if right_side:
        return right_side
    # if here, then no owner found, return None
    return None

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    # if left is None, return node
    if node['left'] == None:
        return node
    # else, recursively call min_node on left side
    return min_node(node['left'])

def delete_owner_logic():
        # get global ownerRoot for use in delete_owner_bst
        global ownerRoot
        # if no owners, print message and return
        if not ownerRoot:
            print("No owners to delete.")
            return
        # first check if to delete owner is in tree, if not, print message and return
        owner_to_delete = input("Owner name: ")
        if not find_owner_bst(ownerRoot, owner_to_delete):
            print(f"Owner '{owner_to_delete}' not found.")
            return
        print(f"Deleting {owner_to_delete}'s entire Pokedex...")
        ownerRoot = delete_owner_bst(ownerRoot, owner_to_delete)
        print("Pokedex deleted.")


def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    # recursively find owner: cannot rely on capital letters, so must check both sides
    # if root is empty, return None
    if root == None:
        return None
    # if owner name is the same as root's owner name, delete, account for children
    if owner_name.lower() == root['owner'].lower():
        # case 1: no children, return None
        if root['left'] == None and root['right'] == None:
            return None
        # case 2: one child, return child
        if root['left'] == None:
            return root['right']
        if root['right'] == None:
            return root['left']
        # case 3: two children, find min right, replace root, delete min right
        min_right = min_node(root['right'])
        root['owner'] = min_right['owner']
        root['pokedex'] = min_right['pokedex']
        root['right'] = delete_owner_bst(root['right'], min_right['owner'])
        return root
    # check BOTH sides to account for edge case in capital letters
    root['left'] = delete_owner_bst(root['left'], owner_name)
    root['right'] = delete_owner_bst(root['right'], owner_name)
    return root


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    if not root:
        return

    # create queue that starts with only root, then as we iterate through, add children in BFS order
    queue = [root]
    while True:
        # pop out first item and print info
        current = queue.pop(0)
        print(f"\nOwner: {current['owner']}")
        display_pokemon_list(current['pokedex'])
        # add any children to queue
        if current['left']:
            queue.append(current['left'])
        if current['right']:
            queue.append(current['right'])
        # This way only checks if we want to exit queue after added potential children, 
        # avoids edge case of only 1 item in queue but has children
        if not queue:
            break

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    # print out root, then left side (recursively), then right side
    # current node:
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root['pokedex'])
    # left side nodes:
    if root['left']:
        pre_order(root['left'])
    # right side nodes:
    if root['right']:
        pre_order(root['right'])

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    # print out leftside, then root, then right side
    # left side nodes:
    if root['left']:
        in_order(root['left'])
    # current node:
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root['pokedex'])
    # right side nodes:
    if root['right']:
        in_order(root['right'])


def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    # print out leftside, then right side, then root
    # left side nodes:
    if root['left']:
        post_order(root['left'])
    # right side nodes:
    if root['right']:
        post_order(root['right'])
    # current node:
    print(f"\nOwner: {root['owner']}")
    display_pokemon_list(root['pokedex'])




########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    # first, get the ID of the Pokemon to add
    ID_choice = read_int_safe("Enter Pokemon ID to add: ")
    # next, get the Pokemon dict by ID
    pokemon_to_add = get_poke_dict_by_id(ID_choice)
    # if the Pokemon is not found, print message and return
    if not pokemon_to_add:
        print(f"ID {ID_choice} not found in Honen data.")
        return
    # if the Pokemon is already in the pokedex, print message and return
    if pokemon_to_add in owner_node['pokedex']:
        print(f"Pokemon already in the list. No changes made.")
        return
    # if the Pokemon is not in the pokedex, add it and print success message
    owner_node['pokedex'].append(pokemon_to_add)
    print(f"Pokemon {pokemon_to_add['Name']} (ID {pokemon_to_add['ID']}) added to {owner_node['owner']}'s Pokedex.")


def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    
    # get the name of the Pokemon to release
    name_choice = input("Enter Pokemon Name to release: ")
    # iterate over list till find the name, then remove it
    for pokemon in owner_node['pokedex']:
        if pokemon['Name'].lower() == name_choice.lower():
            print(f"Releasing {pokemon['Name']} from {owner_node['owner']}.")
            owner_node['pokedex'].remove(pokemon)
            return
    # if not found, print message and return
    print(f"No Pokemon named '{name_choice}' in {owner_node['owner']}'s Pokedex.")


def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    # get name of pokemon to evolve
    name_choice = input("Enter Pokemon Name to evolve: ")
    # 4 cases: not found, cannot evolve, evolution in list, and evolution not in list
    # iterate over list till find the name, then remove it
    for pokemon in owner_node['pokedex']:
        if pokemon['Name'].lower() == name_choice.lower():
            # case: cannot evolve: print message and return
            if pokemon['Can Evolve'] == "FALSE":
                print(f"{pokemon['Name']} cannot evolve.")
                return
            # 2 cases: evolution in list and evolution not in list:
            # call funct to check if ID+1 is in list
            evolution = get_poke_dict_by_id(pokemon['ID'] + 1)
            print(f"Pokemon evolved from {pokemon['Name']} (ID {pokemon['ID']}) to {evolution['Name']} (ID {evolution['ID']}).")

            # case: evolution in list, remove old, print message and return
            if evolution in owner_node['pokedex']:
                # Marshtomp was already present; releasing it immediately.
                print(f"{evolution['Name']} was already present; releasing it immediately.")
                owner_node['pokedex'].remove(pokemon)
                return
            # case: evolution not in list, remove old, add new, return
            owner_node['pokedex'].remove(pokemon)
            owner_node['pokedex'].append(evolution)
            return
    # case: not found, print message and return:
    print(f"No Pokemon named '{name_choice}' in {owner_node['owner']}'s Pokedex.")


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    # if root is None, return empty list
    if root == None:
        return arr
    # recursively gather all owners into the list
    # if left side has children, gather them
    if root['left']:
        arr += gather_all_owners(root['left'], [])
    # append current node's info
    arr.append([root['owner'], len(root['pokedex'])])
    # if right side has children, gather them
    if root['right']:
        arr += gather_all_owners(root['right'], [])
    # return the accumulated list
    return arr

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    global ownerRoot
    # if no owners, print message and return
    if not ownerRoot:
        print("No owners at all.")
        return
    # create empty list to store all owners
    owner_list = []
    # call gather_all_owners to fill the list
    owner_list = gather_all_owners(ownerRoot, owner_list)
    # bubble sort for num pokemon
    for i in range(len(owner_list)):
        for j in range(len(owner_list) - 1):
            if owner_list[j][1] > owner_list[j + 1][1]:
                owner_list[j], owner_list[j + 1] = owner_list[j + 1], owner_list[j]
    # bubble sort for alpha: as if lowercase
    for i in range(len(owner_list)):
        for j in range(len(owner_list) - 1):
            if owner_list[j][1] == owner_list[j + 1][1]:
                if owner_list[j][0].lower() > owner_list[j + 1][0].lower():
                    owner_list[j], owner_list[j + 1] = owner_list[j + 1], owner_list[j]

    for owner in owner_list:
        print(f"Owner: {owner[0]} (has {owner[1]} Pokemon)")

########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    global ownerRoot
    # if no owners, print message and return
    if not ownerRoot:
        print("No owners in the BST.")
        return
    # print menu options and get choice
    print("1) BFS")
    print("2) Pre-order")
    print("3) In-order")
    print("4) Post-order")
    choice = read_int_safe("Your choice: ")
    # call relevant function based on choice
    if choice == PRINT_OWNER_BFS:
        bfs_traversal(ownerRoot)
        return
    elif choice == PRINT_OWNER_PRE:
        pre_order(ownerRoot)
        return
    elif choice == PRINT_OWNER_IN:
        in_order(ownerRoot)
        return
    elif choice == PRINT_OWNER_POST:
        post_order(ownerRoot)
        return
    else:
        print("Invalid choice.")
        return

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

    while True:
        # print menu options
        print("\n-- Display Filter Menu --")
        print("1. Only a certain Type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")
        # get choice and call relecant function
        choice = read_int_safe("Your choice: ")
        if choice == DISP_CERTAIN_TYPE:
            display_certian_type(owner_node['pokedex'])
            pass
        elif choice == DISP_EVOLVABLE:
            display_evolvable(owner_node['pokedex'])
            pass
        elif choice == DISP_ATTACK_ABOVE:
            display_atack_above(owner_node['pokedex'])
            pass
        elif choice == DISP_HP_ABOVE:
            display_hp_above(owner_node['pokedex'])
            pass
        elif choice == DISP_NAME_STARTS:
            display_name_starts(owner_node['pokedex'])
            pass
        elif choice == DISP_ALL:
            display_pokemon_list(owner_node['pokedex'])
            pass
        elif choice == DISP_BACK:
            print("Back to Pokedex Menu.")
            return
        else:
            print("Invalid choice.")


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
        if choice == OWNER_ADD_POKEMON:
            add_pokemon_to_owner(owner_node)
            pass
        elif choice == OWNER_DISPLAY_POKEDEX:
            display_filter_sub_menu(owner_node)
            pass
        elif choice == OWNER_RELEASE_POKEMON:
            release_pokemon_by_name(owner_node)
            pass
        elif choice == OWNER_EVOLVE_POKEMON:
            evolve_pokemon_by_name(owner_node)
            pass
        elif choice == OWNER_BACK:
            print("Back to Main Menu.")
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
        print("4. Display owners by number of Pokemon")
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
            delete_owner_logic()
            pass
        elif choice == MAIN_SORT_OWNERS:
            sort_owners_by_num_pokemon()
            pass
        elif choice == MAIN_PRINT_ALL:
            print_all_owners()
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
