class Assignment:
    def __init__(self, name, assignment_type, score, weight):
        self.name = name
        self.assignment_type = assignment_type
        self.score = score
        self.weight = weight


class Student:
    def __init__(self, name):
        self.name = name
        self.assignments = []
        self.formative_total_weight = 0
        self.summative_total_weight = 0

    def add_assignment(self, assignment):
        if assignment.assignment_type == 'Formative' and self.formative_total_weight + assignment.weight <= 60:
            self.formative_total_weight += assignment.weight
            self.assignments.append(assignment)
        elif assignment.assignment_type == 'Summative' and self.summative_total_weight + assignment.weight <= 40:
            self.summative_total_weight += assignment.weight
            self.assignments.append(assignment)
        else:
            print(f"⚠️ Cannot add {assignment.name}: Weight exceeds limit for {assignment.assignment_type} assignments.")

    def calculate_scores(self):
        formative_score, summative_score = 0, 0
        total_weighted_score = 0
        total_weight = 0
        
        for assignment in self.assignments:
            weighted_score = assignment.score * (assignment.weight / 100)
            total_weighted_score += weighted_score
            total_weight += assignment.weight

            if assignment.assignment_type == 'Formative':
                formative_score += weighted_score
            elif assignment.assignment_type == 'Summative':
                summative_score += weighted_score

        overall_grade = (total_weighted_score / total_weight) * 100 if total_weight > 0 else 0
        gpa = self.convert_to_gpa(overall_grade)
        status = self.check_progression(formative_score, summative_score)

        return formative_score, summative_score, overall_grade, gpa, status

    def convert_to_gpa(self, percentage):
        if percentage >= 85:
            return 5.0
        elif percentage >= 75:
            return 4.0
        elif percentage >= 65:
            return 3.0
        elif percentage >= 50:
            return 2.0
        elif percentage >= 40:
            return 1.0
        else:
            return 0.0  # Failing grade

    def check_progression(self, formative_score, summative_score):
        formative_average = 50  # Define passing average for formative
        summative_average = 50  # Define passing average for summative

        if formative_score >= formative_average and summative_score >= summative_average:
            return "✅ Passed"
        elif formative_score < formative_average and summative_score < summative_average:
            return "❌ Failed - Must Repeat"
        else:
            return "⚠️ Failed - Needs Improvement"

    def resubmission_eligibility(self):
        eligible_assignments = [a for a in self.assignments if a.assignment_type == 'Formative' and a.score < 50]
        return eligible_assignments

    def generate_transcript(self, ascending=True):
        sorted_assignments = sorted(self.assignments, key=lambda a: a.score, reverse=not ascending)
        formative_score, summative_score, overall_grade, gpa, status = self.calculate_scores()

        print(f"\n📜 Transcript for {self.name} ({'Ascending' if ascending else 'Descending'} Order):")
        print("Assignment          Type          Score(%)   Weight(%)")
        print("-" * 50)
        for assignment in sorted_assignments:
            print(f"{assignment.name:<18}{assignment.assignment_type:<12}{assignment.score:<10}{assignment.weight}")
        print("-" * 50)
        print(f"{'Overall Grade':<30}{overall_grade:.2f}%")
        print(f"{'GPA':<30}{gpa:.2f} (Out of 5.0)")
        print(f"{'Course Status':<30}{status}")
        print("-" * 50)


def validate_input(prompt, min_value, max_value, data_type=float):
    while True:
        try:
            value = data_type(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"⚠️ Input must be between {min_value} and {max_value}. Try again.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid number.")


if __name__ == "__main__":
    student_name = input("Enter the student's name: ")
    student = Student(student_name)

    while True:
        name = input("\nEnter assignment name (or 'done' to finish): ")
        if name.lower() == 'done':
            break

        assignment_type = input("Enter type (Formative or Summative): ").capitalize()
        while assignment_type not in ["Formative", "Summative"]:
            print("⚠️ Invalid type. Please enter 'Formative' or 'Summative'.")
            assignment_type = input("Enter type (Formative or Summative): ").capitalize()

        score = validate_input("Enter score (0-100): ", 0, 100)
        weight = validate_input("Enter weight percentage (0-100): ", 0, 100)

        assignment = Assignment(name, assignment_type, score, weight)
        student.add_assignment(assignment)

    formative_score, summative_score, overall_grade, gpa, status = student.calculate_scores()
    print(f"\n📊 Results for {student.name}:")
    print(f"Formative Score: {formative_score:.2f}%")
    print(f"Summative Score: {summative_score:.2f}%")
    print(f"Overall Grade: {overall_grade:.2f}%")
    print(f"GPA: {gpa:.2f} (Out of 5.0)")
    print(f"Course Status: {status}")

    resubmission_assignments = student.resubmission_eligibility()
    if resubmission_assignments:
        print("\n📌 Assignments eligible for resubmission (Formative, score < 50):")
        for a in resubmission_assignments:
            print(f"- {a.name} with score {a.score}%")

    order = input("\nWould you like the transcript in ascending or descending order of scores? (asc/desc): ")
    student.generate_transcript(order == "asc")
