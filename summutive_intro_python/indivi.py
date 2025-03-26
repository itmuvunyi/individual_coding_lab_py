# Class for managing individual assignments
class Assignment:
    def __init__(self, ass_name, ass_cat, weight, grade):
        # Initialize the assignment with name, category, weight, and grade
        self.ass_name = ass_name  
        self.ass_cat = self.normalize_category(ass_cat)  # Normalize category to FA or SA
        self.weight = weight        # The weight of this assignment (out of 100%)
        self.grade = grade          # The grade obtained in the assignment (out of 100%)

    # Calculate the weighted score for the assignment
    def weighted_score(self):
        return (self.weight * self.grade) / 100

    # Normalize the category to ensure it's 'FA' or 'SA'
    @staticmethod
    def normalize_category(category):
        category = category.strip().lower()  # Remove extra spaces and make it lowercase
        if category in ["fa", "formative"]:
            return "FA"
        elif category in ["sa", "summative"]:
            return "SA"
        else:
            return None  # Invalid category


# Class to calculate the overall grade for a student
class StudentCalculateGrade:
    def __init__(self):
        # Initialize with empty assignments and tracking variables
        self.assignments = []
        self.total_weight = 0  # To ensure total weight does not exceed 100%
        self.categories_present = {"FA": False, "SA": False}  # Track if both categories are added

    # Add an assignment to the list
    def add_assignment(self, ass_name, ass_cat, weight, grade):
        category = Assignment.normalize_category(ass_cat)
        
        # Check for valid category, grade, and weight
        if category is None:
            print("Error: Invalid category. Use 'FA' (Formative) or 'SA' (Summative).")
            return
        if grade < 0 or grade > 100:
            print("Error: Grade must be between 0 and 100.")
            return
        if weight < 0 or weight > 100:
            print("Error: Weight must be between 0 and 100.")
            return
        if self.total_weight + weight > 100:
            print("Error: Total weight of assignments must not exceed 100%.")
            return

        # Add the valid assignment
        self.assignments.append(Assignment(ass_name, category, weight, grade))
        self.total_weight += weight
        self.categories_present[category] = True  # Mark the category as entered

    # Calculate the final grade (overall, formative, summative)
    def calculate_final_grade(self):
        category_scores = {"FA": 0, "SA": 0}
        category_weights = {"FA": 0, "SA": 0}
        total_weighted_score = 0

        for assignment in self.assignments:
            weighted_score = assignment.weighted_score()
            category_scores[assignment.ass_cat] += weighted_score
            category_weights[assignment.ass_cat] += assignment.weight
            total_weighted_score += weighted_score

        # Calculate overall grade and category-specific grades
        overall_grade = (total_weighted_score / self.total_weight) * 100 if self.total_weight > 0 else 0
        formative_grade = (category_scores["FA"] / category_weights["FA"]) * 100 if category_weights["FA"] > 0 else 0
        summative_grade = (category_scores["SA"] / category_weights["SA"]) * 100 if category_weights["SA"] > 0 else 0
        
        return overall_grade, formative_grade, summative_grade

    # Calculate GPA based on the final grade
    def calc_gpa(self, final_grade):
        return round((final_grade / 100) * 5, 2)

    # Determine whether the student passes or fails based on the grades
    def deter_fail_pass(self, form_grad, summ_grade):
        avg_the = 50  # The passing threshold for both grades
        if form_grad >= avg_the and summ_grade >= avg_the:
            return "Pass"
        else:
            return "Fail and Repeat!"

    # Show the final results (grades, GPA, pass/fail status)
    def show_results(self):
        # Check if both FA and SA assignments are present
        if not self.categories_present["FA"] or not self.categories_present["SA"]:
            missing = "FA" if not self.categories_present["FA"] else "SA"
            print(f"Error: Missing {missing} category. Please enter both FA and SA assignments.")
            return

        # Get final grades and status
        all_grade, form_grad, summ_grade = self.calculate_final_grade()
        gpa = self.calc_gpa(all_grade)
        pass_fail_status = self.deter_fail_pass(form_grad, summ_grade)

        # Print the results
        print("\nFinal Results:")
        print(f"Overall Grade: {all_grade:.2f}%")
        print(f"Formative Grade: {form_grad:.2f}%")
        print(f"Summative Grade: {summ_grade:.2f}%")
        print(f"GPA: {gpa}")
        print(f"Pass/Fail Status: {pass_fail_status}")


# Main function to run the program
def main():
    calcu = StudentCalculateGrade()  # Create an instance of the grade calculator
    num_ass = int(input("Enter the number of assignments: "))  # Get the number of assignments

    # Loop to input assignments
    for _ in range(num_ass):
        ass_name = input("Assignment Name: ")
        ass_cat = input("Category (Formative[FA]/Summative[SA]): ")
        weight = float(input("Weight (as % of total grade): "))
        grade = float(input("Grade obtained (out of 100): "))

        # Add the assignment to the grade calculator
        calcu.add_assignment(ass_name, ass_cat, weight, grade)

    # Show the final results
    calcu.show_results()


# Run the program if this script is executed
if __name__ == "__main__":
    main()
