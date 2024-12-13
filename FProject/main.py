import csv, os, random, datetime
from helpers import get_int, get_log_int, validate_user
from getpass import getpass

def main():
    sign_in()


def sign_in():
    """
        Main login/registration menu
    """
    print("\n Pick an option:")
    print(
        """
    1) Register
    2) login
    0) Quit
    """
    )

    options()





def register():
    """
    User will input their details 
    and be passed through to a home.csv file 
    """

    while True:
        print("\n Please enter your details:")
        print("""
        Please enter your name and surname
        """)

        name = input(">>> Name: ").capitalize().strip()
        surname = input(">>> Surname: ").capitalize().strip()
        username = input(">>> Username: ").strip()


        while True:
            password = getpass(">>> Password: ")
            confirm_pass = getpass(">>> Confirm Password: ")
            
            if password != confirm_pass:
                print("\n >>> Passwords do not match. Please try again. <<<")
                continue
            
            break


        if not all([name, surname, username, password]):
            print("\n >>> All fields are required. <<<")
            continue
        
        user_details = {"name" : name, "surname": surname, "username": username, "password" :password}
        #Check if file exist, adds if not
        if not os.path.exists("details.csv"):
            with open("details.csv", "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=user_details.keys())
                writer.writeheader()
    
        if user_exists(username):
            print("\n User with this username already exists. Please choose a different username.")
            continue
                    
        # Adds new user
        with open("details.csv", "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=user_details.keys())
            writer.writerow(user_details)
            print(f"""
                
                Welcome {username}
            
            """)

        print("Sucess")
        print(
        """
        Do you want to:

                1) Back
                2) Login
                0) Quit 
        """
        )
        options()


def login():
    if not os.path.exists("details.csv"):
        print("No user information found. Please type 1 to register")
        return options()
    with open("details.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        username = input(">>> Username: ").strip()
        password = getpass(">>> Password: ")
        for row in reader:
            if row["username"] == username and row["password"] == password:
                print()
                game_menu(username)
        else:
            print("""
            >>Incorrect username or password
            """)
            login()
            pass

def game_menu(username):
    """
    Main game menu function.
    
    Args: username (str): Username of the player
    """
    print("Welcome to the Guess Game!")

    while True:
        print("""\n 
        Game menu:
            a. Level 1
            b. Level 2
            c. Level 3
            d. Exit
        """)
        choice = input("Chose an option (a/b/c/d): ").lower()
        
        if choice == "a":
            game_rounds = loading_facts('facts.csv', 'fake_facts.csv')
            total_pounts= game_play(username, game_rounds)

            print("Game Over buddy")
            print(f"You have earned {total_pounts} points in total")
            print(f"Check your records in {username}_records.csv")

            replay = input("Would you like to play angain to increase your score? (yes/no)").lower()
            if replay not in ["yes", "y"]:
                game_menu(username)

        elif choice in ['b', 'c']:
            print("Levels comming soon in version 2.0")

        elif choice == 'd':
            print("Thank you for playing")
            exit()      
        else:
            print("Invalid option. Please try again.")
            
def loading_facts(facts_file, false_facts):
    """
    Load facts from CSV files.
    
    Args:
        facts_file (str): Path to CSV file with correct facts
        fake_facts_file (str): Path to CSV file with fake facts
    """
    #Load fact files 
    correct_facts = []
    with open(facts_file, 'r') as f:
        reader = csv.DictReader(f)
        correct_facts = list(reader)
    fake_facts = []
    with open(false_facts, 'r') as f:
        reader = csv.DictReader(f)
        fake_facts = list(reader)

    # Getting game rounds
    game_rounds = []
    for correct_fact in random.choices(correct_facts):
        # Get 3 random facts from fake facts
        wrong_facts = [fact for fact in fake_facts if fact['false_answers'] and fact['number'] == correct_fact['number']]
        wrong_facts = random.sample(wrong_facts, min(3, len(wrong_facts)))



    # (wrong facts + correct fact)
        round_facts = [
            {'choice_fact': fact['false_answers'], 'is_correct': False} 
            for fact in wrong_facts
        ]
        correct_fact_entry = {
            'choice_fact': correct_fact['correct_answer'], 
            'is_correct': True
        }
        round_facts.append(correct_fact_entry)
        
        # Shuffle facts
        random.shuffle(round_facts)
        
        # Getting the index of the correct answer
        correct_index = -1
        for i, fact in enumerate(round_facts):
            if fact['is_correct'] == True:
                correct_index = i
                break
        game_rounds.append({
            'number': correct_fact['number'],
            'question': correct_fact['question'],
            'correct_answer': correct_fact['correct_answer'],
            'facts': round_facts,
            'correct_index': correct_index
        })
        print(game_rounds)
    
    
    return game_rounds
    








def game_play(username, game_rounds):
    """
    Main game play function.
    
    Args:
        username (str): Username of the player
        game_rounds : Prepared game rounds
    
    Returns:
        int: Total points earned
    """
    total_points = 0
    records_file = f"{username}_records.csv"

    
    # Ensure records file exists
    if not os.path.exists(records_file):
        with open(records_file, 'w', newline='') as r_csv:
            writer = csv.writer(r_csv)
            writer.writerow(['round', 'datetime', 'question', 'user_answer', 'correct_answer', 'points'])
    
    for round_num, round_data in enumerate(game_rounds, 1):
        print(f"\nRound {round_num}:")
        print(f"Question: {round_data['question']}")
        
        # Print facts with numbering
        for i, fact in enumerate(round_data['facts'], 1):
            print(f"{i}. {fact['choice_fact']}")
        
        # Track attempts
        attempts = 0
        points_earned = 0
        
        while attempts < 2:
            try:
                user_choice = int(input("Enter your choice (1-4): "))
                
                # Check if choice is valid
                if 1 <= user_choice <= 4:
                    user_choice -= 1  # Convert to 0-based index
                    
                    # Determine points based on attempts
                    if round_data['facts'][user_choice]['is_correct']:
                        if attempts == 0:
                            points_earned = 3
                        else:
                            points_earned = 1
                        # a recommened way(points_earned = 3 if attempts == 0 else 1) from ai
                        total_points += points_earned
                        print(f"Correct! You earned {points_earned} points.")
                        break
                    else:
                        attempts += 1
                        if attempts < 2:
                            print("Wrong answer. Try again!")
                        else:
                            print("Sorry, you've used both attempts. The correct answer was: " + 
                                  round_data['correct_answer'])
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
            
            # If both attempts are used and still incorrect
            if attempts == 2 and points_earned == 0:
                points_earned = 0
        
        # Record the round in user's records
        with open(records_file, 'a', newline='') as f:
            current_datetime = datetime.datetime.now() # An updated edit
            writer = csv.writer(f)
            writer.writerow([
                round_num,
                current_datetime, 
                round_data['question'], 
                round_data['facts'][user_choice]['choice_fact'], 
                round_data['correct_answer'], 
                points_earned
            ])
    
    # Update game-wide records
    #update_game_records(username, total_points)
    
    return total_points




def options():
    while True:
        try:
            choice = get_log_int(">>> ")
            
            if choice == 1:
                return register()
            elif choice == 2:
                return login()
            elif choice == 0:
                print("\n Goodbye!")
                exit()
            
        except Exception as e:
                print(f"\n An error occurred: {e}")



def validate_login(username, password):
    """
    Validate user credentials
    """

    
    with open("details.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return any(
            row["username"] == username and row["password"] == password 
            for row in reader
        )

def user_exists(username):
    """
    Check if user already exists in the CSV file
    """
    # Check if the user already exists
    with open("details.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return any(row["username"] == username for row in reader) # Return True if ANY of the iteratio return True and False if all == False 






def update_game_records(username, points):
    """
    Update the game-wide records CSV file.
    
    Args:
        username (str): Username of the player
        points (int): Total points earned in the game

    Available in v2
    """

    ...






main()