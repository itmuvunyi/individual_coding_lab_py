# Define a class to store assignment details
class Assignment:
    def __init__(self, ass_name, ass_cat, weight, grade):
        self.name = ass_name  # Store the name of the assignment
        self.ass_cat = self.normalize_category(ass_cat)  # Convert category to uppercase (FA or SA)
        self.weight = weight  # Store the weight of the assignment (percentage)
        self.grade = grade  # Store the grade obtained (0-100)

    # Method to calculate weighted score
    def weighted_score(self):
        return (self.weight * self.grade) / 100  # Formula to calculate weighted score

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


# Define and initialize a class to manage student grade calculations
class StudentCalculatorGrade:
    def __init__(self):
        self.assignments = []  # List to store all assignments
        self.total_weight = 0  # Track the total weight entered
        self.categories_present = {"FA": False, "SA": False}  # Check if FA and SA exist

    # Method to add an assignment
    def add_assignment(self, ass_name, ass_cat, weight, grade):
        # Check if grade is within the valid range (0-100)
        if grade < 0 or grade > 100:
            print("Error: Grade must be between 0 and 100.")
            return
        
        # Check if weight is within the valid range (0-100)
        if weight < 0 or weight > 100:
            print("Error: Weight must be between 0 and 100.")
            return
        
        # Check if total weight exceeds 100%
        if self.total_weight + weight > 100:
            print("Error: Total weight of assignments must not exceed 100%.")
            return  # Stop adding the assignment if total weight exceeds 100%

        # Add assignment to the list
        self.assignments.append(Assignment(ass_name, ass_cat, weight, grade))
        self.total_weight += weight  # Update the total weight
        self.categories_present[ass_cat] = True  # Mark the category as present

    # Method to calculate final grades
    def calculate_fin_grade(self):
        ass_cat_scores = {"FA": 0, "SA": 0}  # Store weighted scores for categories
        ass_weights = {"FA": 0, "SA": 0}  # Store total weights for categories
        total_weighted_score = 0  # Sum of all weighted scores
        over_grade = 0

        # Loop through assignments and calculate scores
        for assignment in self.assignments:
            weighted_score = assignment.weighted_score()  # Get weighted score
            ass_cat_scores[assignment.ass_cat] += weighted_score  # Store per category
            ass_weights[assignment.ass_cat] += assignment.weight  # Store category weight
            total_weighted_score += weighted_score  # Update total weighted score

            # If formative grade is below 50% of weight, reduce overall grade and GPA
            if assignment.ass_cat == "FA" and assignment.grade < 50:
                print(f"Warning: Formative assignment '{assignment.ass_name}' grade is below 50%.")
                over_grade -= (assignment.weight * 0.5)  # Reduce overall grade by half of the weight

        # Check if both FA and SA exist
        if not self.categories_present["FA"] or not self.categories_present["SA"]:
            missing_category = "FA" if not self.categories_present["FA"] else "SA"
            print(f"Error: Cannot calculate GPA. No assignments found in {missing_category} category.")
            return None, None, None  # Return None values if a category is missing

        if self.total_weight > 0:
            over_grade = (total_weighted_score / self.total_weight) * 100
        else:
            over_grade = 0  # Avoid division by zero

        if ass_weights["FA"] > 0:
            form_grade = (ass_cat_scores["FA"] / ass_weights["FA"]) * 100
        else:
            form_grade = 0  # Avoid division by zero

        if ass_weights["SA"] > 0:
            summ_grade = (ass_cat_scores["SA"] / ass_weights["SA"]) * 100
        else:
            summ_grade = 0  # Avoid division by zero

        return over_grade, form_grade, summ_grade  # Return final grades

    # Method to calculate GPA
    def calculate_gpa(self, fin_grade):
        return round((fin_grade / 100) * 5, 2)  # Convert final grade (out of 100) to GPA (out of 5)

    # Method to determine pass or fail status of assignments
    def determine_pass_fail(self, form_grade, summ_grade):
        threshold = 50  # Set pass boundary or threshold 
        if form_grade >= threshold and summ_grade >= threshold:
            return "Pass"  # Student passes if both grades meet the threshold or a limit
        return "Fail and Repeat"  # Otherwise, print student fails

    # Method to display final results
    def show_results(self):
        over_grade, form_grade, summ_grade = self.calculate_fin_grade()

        # Stop execution if calculation failed (FA or SA is missing)
        if over_grade is None:
            return

        # Calculate GPA only if both FA and SA exist
        gpa = self.calculate_gpa(over_grade)
        pass_fail_status = self.determine_pass_fail(form_grade, summ_grade)

        # Print the final results
        print("\nFinal Results:")
        print(f"Overall Grade: {over_grade:.2f}%")
        print(f"Formative Grade: {form_grade:.2f}%")
        print(f"Summative Grade: {summ_grade:.2f}%")
        print(f"GPA: {gpa}")
        print(f"Pass/Fail Status: {pass_fail_status}")


# Main function to run the program
def main():
    calculator = StudentCalculatorGrade()  # Create an instance of Student Grade Calculator
    num_assignments = int(input("Enter the number of assignments: "))  # Prompt user to enter number of assignments

    # Loop to correct assignment details from the user
    for _ in range(num_assignments):
        ass_name = input("Assignment Name: ")  # Ask for assignment name
        ass_cat = input("Category (Formative[FA]/Summative[SA]): ").strip().upper()  # Get category in uppercase
        weight = float(input("Weight (as % of total grade): "))  # Get assignment weight
        grade = float(input("Grade obtained (out of 100): "))  # Get assignment grade

        calculator.add_assignment(ass_name, ass_cat, weight, grade)  # Add assignment to calculator

    # Show final calculated results
    calculator.show_results()


# Run the program only if executed directly
if __name__ == "__main__":
    main()
