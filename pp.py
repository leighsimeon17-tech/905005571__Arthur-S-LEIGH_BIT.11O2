from datetime import datetime


class Patient:
    """Stores one patient's details and vaccination history."""
    next_id = 1
    total_created = 0

    def __init__(self, name, age):
        self.patient_id = f"P{Patient.next_id:04d}"
        Patient.next_id += 1
        Patient.total_created += 1
        self.name = name.strip()
        self.age = int(age)
        self.vaccinations = []

    @classmethod
    def create_sample(cls, name, age):
        """Class method for creating a sample patient."""
        return cls(name, age)

    def update_details(self, name, age):
        """Instance method to update this patient's details."""
        self.name = name.strip()
        self.age = int(age)

    def add_vaccination(self, vaccine, vaccination_date, status):
        """Instance method to add a vaccination record."""
        self.vaccinations.append({
            "vaccine": vaccine.strip(),
            "date": vaccination_date,
            "status": status
        })

    def vaccination_summary(self):
        if not self.vaccinations:
            return "No vaccination entries"
        done = sum(v["status"] == "Completed" for v in self.vaccinations)
        return f"{done}/{len(self.vaccinations)} completed"


class PatientTracker:
    """Runs the terminal menu and manages patient objects."""

    def __init__(self):
        self.patients = []  # List data structure containing Patient objects.
        self.load_samples()

    def load_samples(self):
        p1 = Patient.create_sample("Sample Patient One", 24)
        p1.add_vaccination("COVID-19", "2026-01-15", "Completed")
        p1.add_vaccination("Tetanus", "2026-10-30", "Pending")
        p2 = Patient.create_sample("Sample Patient Two", 31)
        p2.add_vaccination("Hepatitis B", "2026-03-12", "Completed")
        self.patients.extend([p1, p2])

    @staticmethod
    def ask_name():
        while True:
            value = input("Enter patient name: ").strip()
            if value:
                return value
            print("Name cannot be empty.")

    @staticmethod
    def ask_age():
        while True:
            try:
                age = int(input("Enter patient age (0-120): ").strip())
                if 0 <= age <= 120:
                    return age
            except ValueError:
                pass
            print("Invalid age. Enter a whole number from 0 to 120.")

    @staticmethod
    def ask_date():
        while True:
            value = input("Enter vaccination date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                print("Invalid date. Example: 2026-10-30")

    def find_patient(self, patient_id):
        return next((p for p in self.patients
                     if p.patient_id.lower() == patient_id.lower()), None)

    def display_patients(self, records=None):
        records = self.patients if records is None else records
        if not records:
            print("\\nNo patient records found.")
            return
        print("\\n" + "-" * 78)
        print(f"{'PATIENT ID':<14}{'NAME':<30}{'AGE':<8}VACCINATION SUMMARY")
        print("-" * 78)
        for p in records:
            print(f"{p.patient_id:<14}{p.name[:28]:<30}{p.age:<8}{p.vaccination_summary()}")
        print("-" * 78)

    def add_patient(self):
        print("\\n--- REGISTER A PATIENT ---")
        patient = Patient(self.ask_name(), self.ask_age())
        self.patients.append(patient)
        print(f"Patient registered. New patient ID: {patient.patient_id}")

    def update_patient(self):
        print("\\n--- UPDATE PATIENT ---")
        patient = self.find_patient(input("Enter patient ID: ").strip())
        if not patient:
            print("Patient not found.")
            return
        print(f"Updating {patient.name}.")
        patient.update_details(self.ask_name(), self.ask_age())
        print("Patient details updated.")

    def delete_patient(self):
        print("\\n--- DELETE PATIENT ---")
        patient = self.find_patient(input("Enter patient ID: ").strip())
        if not patient:
            print("Patient not found.")
            return
        confirm = input(f"Delete {patient.name}? Type YES to confirm: ").strip()
        if confirm == "YES":
            self.patients.remove(patient)
            print("Patient deleted.")
        else:
            print("Deletion cancelled.")

    def search_patients(self):
        print("\\n--- SEARCH PATIENTS ---")
        query = input("Enter patient name or ID: ").strip().lower()
        if not query:
            print("Search cannot be empty.")
            return
        matches = [p for p in self.patients
                   if query in p.name.lower() or query in p.patient_id.lower()]
        self.display_patients(matches)

    def add_vaccination(self):
        print("\\n--- ADD VACCINATION ---")
        patient = self.find_patient(input("Enter patient ID: ").strip())
        if not patient:
            print("Patient not found.")
            return
        print(f"Patient: {patient.name} ({patient.patient_id})")
        while True:
            vaccine = input("Enter vaccine name: ").strip()
            if vaccine:
                break
            print("Vaccine name cannot be empty.")
        vaccination_date = self.ask_date()
        while True:
            status = input("Enter status (Completed/Pending): ").strip().title()
            if status in ("Completed", "Pending"):
                break
            print("Enter either Completed or Pending.")
        patient.add_vaccination(vaccine, vaccination_date, status)
        print("Vaccination record added.")

    def view_vaccinations(self):
        print("\\n--- VACCINATION HISTORY ---")
        patient = self.find_patient(input("Enter patient ID: ").strip())
        if not patient:
            print("Patient not found.")
            return
        print(f"History for {patient.name} ({patient.patient_id})")
        if not patient.vaccinations:
            print("No vaccination records.")
            return
        print(f"{'VACCINE':<28}{'DATE':<18}STATUS")
        print("-" * 62)
        for item in patient.vaccinations:
            print(f"{item['vaccine'][:26]:<28}{item['date']:<18}{item['status']}")

    @staticmethod
    def show_menu():
        print("\\n" + "=" * 52)
        print(" PATIENT RECORD & VACCINATION TRACKER")
        print("=" * 52)
        print("1. Register a new patient")
        print("2. View all patients")
        print("3. Search for a patient")
        print("4. Update patient details")
        print("5. Delete a patient")
        print("6. Add a vaccination record")
        print("7. View vaccination history")
        print("8. Exit")
        print("=" * 52)

    def run(self):
        print("Welcome to the Patient Record and Vaccination Tracker.")
        print("Educational demo only. Use fictional data, not real patient details.")
        actions = {
            "1": self.add_patient,
            "2": self.display_patients,
            "3": self.search_patients,
            "4": self.update_patient,
            "5": self.delete_patient,
            "6": self.add_vaccination,
            "7": self.view_vaccinations
        }
        while True:
            self.show_menu()
            choice = input("Choose an option (1-8): ").strip()
            if choice == "8":
                print("Program closing. Goodbye.")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid option. Choose a number from 1 to 8.")
                continue
            action()
            input("\\nPress ENTER to return to the main menu...")


def main():
    PatientTracker().run()


if __name__ == "__main__":
    main()