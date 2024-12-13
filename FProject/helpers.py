import csv

def main():
    """
        Helper is a function that helps with effecency 
    """
    ...

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


def get_log_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value in [1, 2, 0]:
                return value


        except ValueError:
            pass
        except EOFError:
            break

def validate_user(fname: str, lname: str, uname : str,pword: str, cpword: str) -> int :
    """
    Arg: Takes in user details and checks if they are valid \n
    Return: Return a number 1 or 0 \n
    Data: The information taken will be passed into a csc file i a Dic formate 
    """
    return 1


def user_exists(username):
    """
    Check if user already exists in the CSV file
    """

    with open("details.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return any(row["username"] == username for row in reader)


if __name__ == "__main__":
    main()