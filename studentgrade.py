import json

class Student:
    def __init__(self, name, student_id, reg_no):
        self.name = name
        self.student_id = student_id
        self.reg_no = reg_no
        self.grades = {}

    def add_grade(self, subject, grade):
        """Add a grade for a specific subject."""
        if subject in self.grades:
            self.grades[subject].append(grade)
        else:
            self.grades[subject] = [grade]
        print(f"Added grade {grade} for {subject}.")

    def calculate_average(self):
        """Calculate the average grade across all subjects."""
        total_grades = []
        for grades in self.grades.values():
            total_grades.extend(grades)
        if total_grades:
            return sum(total_grades) / len(total_grades)
        return 0

    def get_letter_grade(self, average):
        """Convert average grade to letter grade."""
        if average >= 90:
            return 'A'
        elif average >= 80:
            return 'B'
        elif average >= 70:
            return 'C'
        elif average >= 60:
            return 'D'
        else:
            return 'F'

    def get_gpa(self, average):
        """Convert average grade to GPA (on a 4.0 scale)."""
        if average >= 90:
            return 4.0
        elif average >= 80:
            return 3.0
        elif average >= 70:
            return 2.0
        elif average >= 60:
            return 1.0
        else:
            return 0.0

    def display_grades(self):
        """Display all grades and their average."""
        print(f"\nStudent: {self.name}")
        print(f"Student ID: {self.student_id}")
        print(f"Registration Number: {self.reg_no}")
        print("Grades Summary:")
        for subject, grades in self.grades.items():
            print(f"{subject}: {grades}")
        average = self.calculate_average()
        letter_grade = self.get_letter_grade(average)
        gpa = self.get_gpa(average)
        print(f"\nAverage Grade: {average:.2f}")
        print(f"Letter Grade: {letter_grade}")
        print(f"GPA: {gpa:.2f}")

    def to_dict(self):
        """Convert student object to a dictionary for saving to a file."""
        return {
            'name': self.name,
            'student_id': self.student_id,
            'reg_no': self.reg_no,
            'grades': self.grades
        }

    @classmethod
    def from_dict(cls, data):
        """Create a student object from a dictionary when loading from a file."""
        student = cls(data['name'], data['student_id'], data['reg_no'])
        student.grades = data['grades']
        return student

def save_students(students, filename):
    """Save student data to a file."""
    student_data = [student.to_dict() for student in students]
    with open(filename, 'w') as file:
        json.dump(student_data, file, indent=4)
    print("Student data saved successfully.")

def load_students(filename):
    """Load student data from a file."""
    try:
        with open(filename, 'r') as file:
            student_data = json.load(file)
        students = [Student.from_dict(data) for data in student_data]
        return students
    except FileNotFoundError:
        return []

def display_grade_statistics(students):
    """Display grade statistics for all students."""
    all_averages = [student.calculate_average() for student in students]
    
    if all_averages:
        highest_average = max(all_averages)
        lowest_average = min(all_averages)
        class_average = sum(all_averages) / len(all_averages)
    else:
        highest_average = lowest_average = class_average = 0
    
    print("\nGrade Statistics:")
    print(f"Highest Average: {highest_average:.2f}")
    print(f"Lowest Average: {lowest_average:.2f}")
    print(f"Class Average: {class_average:.2f}")

def main():
    students = load_students('student_data.json')

    while True:
        print("\nStudent Grades Tracker")
        print("1. Add Student")
        print("2. Add Grade")
        print("3. Display Grades")
        print("4. Display Grade Statistics")
        print("5. Save and Exit")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            reg_no = input("Enter registration number: ")
            student = Student(name, student_id, reg_no)
            students.append(student)
            print("Student added successfully.")
        elif choice == '2':
            print("\nSelect a student to add grades:")
            for i, student in enumerate(students):
                print(f"{i+1}. {student.name} ({student.reg_no})")
            student_index = int(input("Enter the number: ")) - 1
            if 0 <= student_index < len(students):
                subject = input("Enter the subject: ")
                grade = float(input("Enter the grade: "))
                students[student_index].add_grade(subject, grade)
            else:
                print("Invalid student selection.")
        elif choice == '3':
            print("\nSelect a student to view grades:")
            for i, student in enumerate(students):
                print(f"{i+1}. {student.name} ({student.reg_no})")
            student_index = int(input("Enter the number: ")) - 1
            if 0 <= student_index < len(students):
                students[student_index].display_grades()
            else:
                print("Invalid student selection.")
        elif choice == '4':
            display_grade_statistics(students)
        elif choice == '5':
            save_students(students, 'student_data.json')
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
