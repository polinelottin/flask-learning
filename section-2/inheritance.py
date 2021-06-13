class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        marks = []

    def average(self):
        return sum(self.marks)/len(self.marks)

    def friend(self, friend_name):
        return Student(friend_name, self.school)