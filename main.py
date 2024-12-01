from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Key, Controller
import win32gui
import win32com.client
import subprocess
import random

# Initialize thae keyboard controller
keyboard = Controller()

# Key mappings
KEY_MAPPING = {
    "a": "a",         # Move left
    "d": "d",         # Move right
    "space": Key.space  # Attack
}

# Frame data for moves
FRAME_DATA = {
    "neutral_attack": {
        "state": "idle",
        "command": "Neutral + Attack",
        "startup": 5,
        "active": 2,
        "recovery": 16,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
    "move_left": {
        "state": "moving",
        "command": "Move Left",
        "startup": 0,
        "active": 0,
        "recovery": 0,
        "can_cancel": False,
        "KO": False,
    },
    "move_right": {
        "state": "moving",
        "command": "Move Right",
        "startup": 0,
        "active": 0,
        "recovery": 0,
        "can_cancel": False,
        "KO": False,
    },
    "forward_attack": {
        "state": "forward",
        "command": "Forward + Attack",
        "startup": 4,
        "active": 3,
        "recovery": 15,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
    "backward_attack": {
        "state": "backward",
        "command": "Backward + Attack",
        "startup": 6,
        "active": 2,
        "recovery": 20,
        "can_cancel": True,  # Can cancel into another move
        "KO": False,
    },
}

game_starting = 'False'

# Focus the game window
def focus_game_window():
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("FOOTSIES")  # Replace with your game's window title
        print("Game window focused.")
    except Exception as e:
        print(f"Failed to focus game window: {e}")


# Launch the game
def launch_game():
    try:
        game_process = subprocess.Popen(r"C:\Users\ardui\Downloads\FOOTSIES_v1_5_0\FOOTSIES_v1_5_0\FOOTSIES.exe", shell=True)
        if game_process is None:
            raise ValueError("Failed to start the game process.")
        print("Game launched.")
        return game_process
    except Exception as e:
        print(f"Error launching the game: {e}")
        return None

class TreeNode:
    def __init__(self, name, value=None):
        """
        Initializes a node in the tree.

        :param name: Name of the node.
        :param value: The value of the node, used in minimax (default is None).
        """
        self.name = name
        self.value = value  # This value is used for terminal nodes in Minimax
        self.children = []

    def add_child(self, child_node):
        """
        Adds a child to the current node.
        :param child_node: Instance of TreeNode.
        """
        self.children.append(child_node)


def create_tree_for_attack():
    """
    Creates a tree structure similar to the one in the image.

    :return: The root of the tree.
    """
    # Root node
    root = TreeNode("Root")

    # First level
    move_backward = TreeNode("move_left")
    attack = TreeNode("neutral_attack")
    move_forward = TreeNode("move_right")
    root.add_child(move_backward)
    root.add_child(attack)
    root.add_child(move_forward)

    # Second level for "Move Backward"
    move_backward.add_child(TreeNode("move_left"))
    move_backward.add_child(TreeNode("neutral_attack"))
    move_backward.add_child(TreeNode("move_right"))

    # Second level for "Attack"
    attack.add_child(TreeNode("move_left"))
    attack.add_child(TreeNode("neutral_attack"))
    attack.add_child(TreeNode("move_right"))

    # Second level for "Move Forward"
    move_forward.add_child(TreeNode("move_left"))
    move_forward.add_child(TreeNode("neutral_attack"))
    move_forward.add_child(TreeNode("move_right"))

    return root



# Leaf node values
def assign_tree_values(tree, move_names):
    """
    Assigns evaluation scores to the tree's leaf nodes based on the move names.

    :param tree: The root node of the tree.
    :param move_names: List of move names corresponding to the tree structure.
    """
    for i, child in enumerate(tree.children):
        for j, grandchild in enumerate(child.children):
            move_name = move_names[i][j]
            grandchild.value = evaluation_function(move_name)

def evaluation_function(move_name):
    """
    Evaluate the value of a move based on its frame data.

    :param move_name: The name of the move to evaluate (key in FRAME_DATA).
    :return: The calculated score for the move.
    """
    if move_name not in FRAME_DATA:
        raise ValueError(f"Move {move_name} not found in frame data.")
    
    # Extract frame data for the move
    move_data = FRAME_DATA[move_name]
    startup = move_data["startup"]
    active = move_data["active"]
    recovery = move_data["recovery"]
    can_cancel = move_data["can_cancel"]
    is_ko = move_data["KO"]

    # Calculate the score
    score = (
        (10 / (startup + 1))  # Faster startup is better
        + (2 * active)        # Active frames are weighted positively
        - (recovery / 2)      # Recovery time is weighted negatively
    )
    # Bonus for moves that can cancel
    if can_cancel:
        score += 5

    # Bonus for KO moves
    if is_ko:
        score += 10

    return score


def minimax_alpha_beta(node, depth, is_maximizing, alpha, beta):
    # Base case: If the node is a leaf node, return its value and itself
    if not node.children:
        return node.value, node

    best_node = None
    if is_maximizing:
        max_eval = float('-inf')
        for child in node.children:
            eval, _ = minimax_alpha_beta(child, depth + 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_node = child
            alpha = max(alpha, eval)
            if beta <= alpha:  # Prune the remaining branches
                break
        return max_eval, best_node
    else:
        min_eval = float('inf')
        for child in node.children:
            eval, _ = minimax_alpha_beta(child, depth + 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_node = child
            beta = min(beta, eval)
            if beta <= alpha:  # Prune the remaining branches
                break
        return min_eval, best_node

# Perform an action using `pynput`
def perform_action(action):
    focus_game_window()  # Ensure the game is focused before sending input
    if action == 'neutral_attack':
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        print("Pressed 'space' - Performed neutral attack")
    elif action == 'move_right':
        keyboard.press(KEY_MAPPING["d"])
        keyboard.release(KEY_MAPPING["d"])
        print("Pressed 'd' - Moved right")
    elif action == 'move_left':
        keyboard.press(KEY_MAPPING["a"])
        keyboard.release(KEY_MAPPING["a"])
        print("Pressed 'a' - Moved left")
    elif action == 'forward_attack':
        keyboard.press(KEY_MAPPING["d"])
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        if FRAME_DATA["forward_attack"]["can_cancel"]:
            keyboard.press(KEY_MAPPING["space"])  # Perform cancel attack
            keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["d"])
        print("Pressed 'd' and 'space' twice - Performed forward attack combo")
    elif action == 'backward_attack':
        keyboard.press(KEY_MAPPING["a"])
        keyboard.press(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["space"])
        if FRAME_DATA["backward_attack"]["can_cancel"]:
            keyboard.press(KEY_MAPPING["space"])  # Perform cancel attack
            keyboard.release(KEY_MAPPING["space"])
        keyboard.release(KEY_MAPPING["a"])
        print("Pressed 'a' and 'space' twice - Performed backward attack combo")
    else:
        print(f"Unknown action: {action}")


# Get possible moves based on the bot's movement state
def get_possible_moves(movement_state):
    if movement_state == 'idle':
        return ["neutral_attack", "move_left", "move_right"]
    return ["forward_attack", "backward_attack", "move_left", "move_right"]

click_count = 0
def on_click(x, y, button, pressed):
    global game_starting
    global click_count
    if pressed:  # Mouse clicked
        click_count += 1
        print(f"Mouse clicked at ({x}, {y}). Starting the game...")
        if click_count >= 2:
            game_starting = True
            return False 

move_names = [
    ["move_left", "neutral_attack", "move_right"],  # For "Move Backward" branch
    ["move_left", "neutral_attack", "move_right"], # For "Attack" branch
    ["move_left", "neutral_attack", "move_right"], # For "Move Forward" branch
]
tree = create_tree_for_attack()
assign_tree_values(tree, move_names)


# Main loop
def main():
    # Launch the game and start the bot immediately
    game_process = launch_game()
    if not game_process:
        print("Failed to launch the game. Exiting.")
        return
    
    print("Waiting for mouse click to start the game...")
    with MouseListener(on_click=on_click) as listener:
        listener.join()  # Wait until the listener stops

    movement_state = 'idle'
    
    try:
        while True:
            # Check if the game has exited
            if game_process.poll() is not None:
                print("Game has exited. Shutting down the bot...")
                break
              
            # Get possible moves
            possible_moves = get_possible_moves(movement_state)
            
            # Get the optimized move
            optimize_value, best_node = minimax_alpha_beta(tree, depth=0, is_maximizing=True, alpha=float('-inf'), beta=float('inf'))
            print(f"Optimized value: {optimize_value}, Best move: {best_node.name}")

            # Perform the best action
            perform_action(best_node.name)

            # Update movement state for next iteration
            if best_node.name in ["move_left", "move_right"]:
                movement_state = "moving"
            else:
                movement_state = "idle"

    except KeyboardInterrupt:
        print("Exiting due to user interruption.")
    finally:
        if game_process.poll() is None:
            game_process.terminate()
        print("Bot and game process terminated.")


if __name__ == "__main__":
    main()
