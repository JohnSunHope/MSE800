class Students:
    def __init__(self):
        self.students = {}

    def add_student(self, name, age, id):
        self.students[id] = {"name": name, "age": age}
    
    def get_student(self, id):
        return self.students.get(id)
    
    def get_all_students(self):
        return self.students
    
    def remove_student(self, id):
        if id in self.students:
            del self.students[id]
            return True
        else:
            return False

def main():
    students = Students()
    students.add_student("Elbert", 28, 1001)
    students.add_student("KOKO", 28, 1002)
    print(students.get_all_students())

if __name__ == '__main__':
    main()