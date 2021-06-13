def who_do_you_know():
    answer = input("friends sep. by space: ")

    people_list = answer.split(", ")
    people_without_spaces = [person.strip().lower() for person in people_list]
    return people_without_spaces

def ask_user():
    name = input("name: ")
    known_people = who_do_you_know()

    if name.lower() in known_people:
        print("known")

ask_user()