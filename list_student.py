# Global variable to store student objects
student_list = []


# Class definition (without __init__)
class Student:
    # Function to set student data
    def set_data(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

    # Function to display student info
    def display_info(self):
        return f"Name: {self.name}, Age: {self.age}"


def input_student_info(x, name=None, age=None, student_id=None):
    print(f"Student {x}")

    # Local variables
    if not name:
        _name = input("Enter student name: ")
    else:
        _name = name
    if not age:
        _age = int(input("Enter student age: "))
    else:
        _age = age
    if not student_id:
        _student_id = input("Enter student ID: ")
    else:
        _student_id = student_id

    student = Student()

    # Set data using class function
    student.set_data(_name, _age, _student_id)

    # Add student to global list
    student_list.append(student)

    print()


# Function to collect student data
def collect_students():
    print("Enter details for at least 3 students:\n")

    for i in range(3):
        try:
            input_student_info(i + 1)
        except Exception:
            print("Something went wrong with input. Please try again.")
            input_student_info(i + 1)
            continue


# Function to display students in order
def display_students():
    print("\nList of Students (Names and Ages):")

    # Sort students by name
    sorted_students = sorted(student_list, key=lambda s: s.name)

    for student in sorted_students:
        print(student.display_info())


# Standard Python entry point as main function
if __name__ == "__main__":
    collect_students()
    display_students()
