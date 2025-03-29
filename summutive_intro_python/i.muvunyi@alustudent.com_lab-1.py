"""
Innocent Tito Muvunyi: Lab 1: Grade Generator Calculator Project 
 
# Define a class to store assignment details"
"""
# Define the Assignment class which represents an individual assignment
class Assignment:
    def __init__(self, ass_name, ass_cat, weight, grade):
        # Initialize the assignment with name, category, weight, and grade
        self.name = ass_name  # Store the assignment name
        self.ass_cat = self.normalize_category(ass_cat)  # Normalize the category (FA or SA)
        self.weight = weight  # Store the weight of the assignment
        self.grade = grade  # Store the grade received for the assignment

    # Calculate the weighted score for the assignment
    def weighted_score(self):
        return (self.weight * self.grade) / 100  # Weight * grade divided by 100 gives the weighted score

    # Normalize category input (allowing different case or full-form input)
    @staticmethod
    def normalize_category(category):
        category = category.strip().upper()  # Strip and convert to uppercase to avoid case sensitivity
        if category in ["FA", "FORMATIVE"]:
            return "FA"  # Return 'FA' for formative assignments
        elif category in ["SA", "SUMMATIVE"]:
            return "SA"  # Return 'SA' for summative assignments
        else:
            return None  # Return None if the category is invalid


# Define the StudentCalculatorGrade class to manage grade calculations
class StudentCalculatorGrade:
    def __init__(self, student_name, class_name):
        # Initialize the student grade calculator with student and class info
        self.student_name = student_name
        self.class_name = class_name
        self.assignments = []  # List to hold all assignments for the student
        self.total_weight = 0  # Total weight for all assignments
        self.categories_present = {"FA": False, "SA": False}  # Flags for whether categories exist

    # Method to add an assignment to the grade calculator
    def add_assignment(self, ass_name, ass_cat, weight, grade):
        if not (0 <= grade <= 100):  # Check if the grade is between 0 and 100
            print("⚠️", "Grade must be between 0 and 100.")
            return
        if not (0 <= weight <= 100):  # Check if the weight is between 0 and 100
            print("⚠️", "Weight must be between 0 and 100.")
            return
        if self.total_weight + weight > 100:  # Check if total weight exceeds 100
            print("⚠️", "Total weight cannot exceed 100%.")
            return

        # Create the assignment object and append to the assignments list
        assignment = Assignment(ass_name, ass_cat, weight, grade)
        self.assignments.append(assignment)
        self.total_weight += weight  # Update total weight
        if assignment.ass_cat:  # Check if the category is valid (FA or SA)
            self.categories_present[assignment.ass_cat] = True

    # Method to calculate final grade and GPA
    def calculate_fin_grade(self):
        ass_cat_scores = {"FA": 0, "SA": 0}  # Initialize scores for formative and summative categories
        ass_weights = {"FA": 0, "SA": 0}  # Initialize weights for formative and summative categories
        total_weighted_score = 0  # Total weighted score across all assignments

        # Loop through all assignments and calculate weighted scores
        for assignment in self.assignments:
            weighted_score = assignment.weighted_score()  # Calculate weighted score for each assignment
            ass_cat_scores[assignment.ass_cat] += weighted_score  # Accumulate scores by category
            ass_weights[assignment.ass_cat] += assignment.weight  # Accumulate weights by category
            total_weighted_score += weighted_score  # Add to total weighted score

        # Check if both formative (FA) and summative (SA) categories are present
        if not self.categories_present["FA"] or not self.categories_present["SA"]:
            print("⚠️", "Cannot calculate GPA. Missing FA or SA category.")
            return None, None, None, None

        # Calculate final grades
        overall_grade = (total_weighted_score / self.total_weight) * 100 if self.total_weight > 0 else 0
        formative_grade = (ass_cat_scores["FA"] / ass_weights["FA"]) * 100 if ass_weights["FA"] > 0 else 0
        summative_grade = (ass_cat_scores["SA"] / ass_weights["SA"]) * 100 if ass_weights["SA"] > 0 else 0
        gpa = self.convert_to_gpa(overall_grade)  # Convert overall grade to GPA
        return overall_grade, formative_grade, summative_grade, gpa

    # Method to convert percentage grade to GPA
    def convert_to_gpa(self, percentage):
        if percentage >= 85:
            return 4.0  # Highest GPA
        elif percentage >= 75:
            return 3.5  # Second highest GPA
        elif percentage >= 65:
            return 3.0  # Middle GPA
        elif percentage >= 50:
            return 2.5  # Passing GPA
        elif percentage >= 40:
            return 2.0  # Minimum passing GPA
        else:
            return 0.0  # Fail GPA

    # Method to determine pass or fail status based on grades
    def determine_pass_fail(self, form_grade, summ_grade):
        if form_grade >= 50 and summ_grade >= 50:  # If both formative and summative grades are 50 or more
            return "\033[92m Pass\033[0m"  # Return "Pass" in green color
        return "\033[91m Fail and Retake\033[0m"  # Return "Fail and Retake" in red color 

    # Method to display the student's transcript
    def display_transcript(self):
        overall_grade, _, _, gpa = self.calculate_fin_grade()
        
        if overall_grade is None:
            print("⚠️ Unable to display transcript due to missing grades.")
            return

        print(f"\n📜 Transcript\nStudent Name: {self.student_name} \nCohort: {self.class_name}")
        print(f"\n{'Assignment':<15}{'Category':<15}{'Grade (%)':<12}{'Weight (%)'}")
        print("-" * 50)

        # Loop through all assignments and display them
        for assignment in self.assignments:
            print(f"{assignment.name:<15}{assignment.ass_cat:<15}{assignment.grade:<12.2f}{assignment.weight:.2f}")
        
        print("-" * 50)
        print(f"{'Overall Grade':<30}{overall_grade:.2f}%")
        print(f"{'GPA':<30}{gpa:.2f}")
        print("-" * 50)

    # Method to show final results
    def show_results(self):
        over_grade, form_grade, summ_grade, gpa = self.calculate_fin_grade()
        if over_grade is None:
            return
        # Determine the color for GPA based on its value
        gpa_color = "\033[91m" if gpa <= 2.0 else "\033[93m" if gpa <= 3.0 else "\033[92m"
        print("\n🎓 Final Results:") 
        print(f"Overall Grade: {over_grade:.2f}%")
        print(f"Formative Grade: {form_grade:.2f}%")
        print(f"Summative Grade: {summ_grade:.2f}%")
        print(f"GPA: {gpa_color}{gpa:.2f}\033[0m")
        print(f"Courses Status: {self.determine_pass_fail(form_grade, summ_grade)}")


# Main function to run the grade calculator system
def main():
    print("🎉 Welcome to the Grade Calculator System!")  # Introduction message with a welcoming emoji
    student_name = input("Enter Student's Code or Name: ")  # Ask for student's name
    class_name = input("Enter Class or Cohort Name: ")  # Ask for class name
    grade_calculator = StudentCalculatorGrade(student_name, class_name)  # Initialize the grade calculator object

    # Loop to allow adding multiple assignments
    while True:
        ass_name = input("Enter Assignment Name: ")  # Prompt for assignment name
        ass_cat = input("Enter Assignment Category (Formative[FA]/Summative[SA]): ")  # Prompt for assignment category
        weight = float(input("Enter Assignment Weight (as % of total grade): "))  # Prompt for assignment weight
        grade = float(input("Enter Assignment Grade (out of 100): "))  # Prompt for assignment grade

        # Add the assignment to the grade calculator
        grade_calculator.add_assignment(ass_name, ass_cat, weight, grade)

        # Ask if the user wants to add another assignment
        another = input("Do you want to add another assignment? (y/n): ").strip().lower()
        if another != "y":
            break  # Exit the loop if user does not want to add more assignments

    # Show the final results and the student's transcript
    grade_calculator.show_results()
    grade_calculator.display_transcript()


# Run the main function to start the grade calculator
if __name__ == "__main__":
    main()
