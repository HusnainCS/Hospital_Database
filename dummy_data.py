# ----------- LIBRARIES -----------

from sqlalchemy import create_engine, text  # A library that lets us connect to and work with the database.
from faker import Faker  # Library to generate fake data like names, addresses, phone numbers, etc.
from tqdm import tqdm  # Shows a nice progress bar while inserting data.
import random  # Helps choose random values (e.g., male/female).
from datetime import datetime  # To calculate the patient's age from their date of birth.

# ----------- DATABASE CONNECTION -----------

DB_USER = 'hospital_db'
DB_PASSWORD = 'redgroup123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = "hospital_db"

# creates a connection engine that Python uses to send data to PostgreSQL.
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

fake = Faker('en_PK')
def generate_pak_number(): return f"03{random.randint(0,9)}{random.randint(1000000,9999999)}"

# ----------- FUNCTION TO GENERATE NAME & NUMBER -----------
def generate_pakistani_name_and_number():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name, 

def reset_sequences():
    tables = [
        ('patient', 'patient_id'), 
        ('doctor', 'doctor_id'), 
        ('appointment', 'appointment_id'), 
        ('reception', 'receptionist_id'), 
        ('department', 'department_id'), 
        ('laboratory', 'test_id'),  
        ('staff', 'staff_id'), 
        ('prescription', 'prescription_id'),
        ('administrator', 'admin_id'), 
        ('medical_history', 'record_id'), 
        ('medicine', 'medicine_id'), 
        ('supplier', 'supplier_id'), 
        ('room', 'room_id'), 
        ('payment', 'payment_id'), 
        ('parking', 'driver_id')
    ]
    
    with engine.begin() as conn:
        for table, id_column in tables:
            try:
                # Get the actual sequence name from PostgreSQL
                seq_query = text(f"""
                    SELECT pg_get_serial_sequence('{table}', '{id_column}');
                """)
                seq_name = conn.execute(seq_query).scalar()
                
                if seq_name:
                    # Extract just the sequence name without schema
                    seq_name = seq_name.split('.')[-1] if '.' in seq_name else seq_name
                    conn.execute(text(f"ALTER SEQUENCE {seq_name} RESTART WITH 1"))
                    print(f"Reset sequence for {table} (using {seq_name})")
                else:
                    print(f"No sequence found for {table}.{id_column}")
            except Exception as e:
                print(f"Could not reset sequence for {table}: {e}")
          # Continue to next table instead of aborting
                    
# ----------- INSERT PATIENT DATA FUNCTION -----------
def insert_patient(n=1000000):  # Change to 100000 if needed
    with engine.begin() as conn:
        for _ in tqdm(range(n), desc='Inserting Patient Data...'):
            first_name = fake.first_name()
            last_name = fake.last_name()
            contact_number = generate_pak_number()
            date_of_birth = fake.date_of_birth(minimum_age=1, maximum_age=90)
            gender = random.choice(['Male', 'Female'])
            today = datetime.now()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            email = fake.email()
            address = fake.address()

            query = text("""
                INSERT INTO patient (first_name, last_name, date_of_birth, gender, age, contact_number, email, address) 
                VALUES (:first_name, :last_name, :date_of_birth, :gender, :age, :contact_number, :email, :address)
            """)

            conn.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth,
                'gender': gender,
                'age': age,
                'contact_number': generate_pak_number(),
                'email': email,
                'address': address
            })
    print("✅ Dummy Patient Data Inserted")


# # -------- DOCTOR DATA --------
def insert_doctor(n=50000):
    specialities = ['Cardiology', 'Neurology', 'Orthopedics', 'ENT', 'Oncology', 'Dermatology', 'Pediatrics']

    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting Doctor Data Please Wait.....!"):
            first_name = 'Dr.'
            last_name = fake.last_name()
            speciality = random.choice(specialities)
            email = fake.email()
            contact_no = generate_pak_number()

            query = text("""INSERT INTO doctor (first_name, last_name, speciality, email, contact_no)
                         VALUES (:first_name, :last_name, :speciality, :email, :contact_no)""")

            conn.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'speciality': speciality,
                'email': email,
                'contact_no': contact_no
            })
    print("Dummy Doctor Data Inserted")


# -------- APPOINTMENT DATA --------
def insert_appointment(n=1000000):
    with engine.begin() as conn:
        # Check if the patients table exists and contains data
        table_check = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'patient')")).scalar()
        if not table_check:
            print("The 'patient' table does not exist. Please create the table first.")
            return

        patient_ids = conn.execute(text("SELECT patient_id FROM patient")).fetchall()
        doctor_ids = conn.execute(text("SELECT doctor_id FROM doctor")).fetchall()
        # comprehensions convert the list of tuples [(1,), (2,), (3,)...] into a simple list like [1, 2, 3,...]
        patient_ids = [row[0] for row in patient_ids]
        doctor_ids = [row[0] for row in doctor_ids]

        if not patient_ids or not doctor_ids:
            print("No Patient or Doctors found! Insert them first.")
            return
        
        for _ in tqdm(range(n), desc="Inserting Appointment Data Please Wait......"):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            appointment_date = fake.date_between(start_date='-1y', end_date='today')
            appointment_time = fake.time()
            appointment_status = random.choice(['Scheduled', 'Completed', 'Cancelled'])

            query = text("""INSERT INTO appointment (patient_id, doctor_id, appointment_date, appointment_time, appointment_status) 
                         VALUES (:patient_id, :doctor_id, :appointment_date, :appointment_time, :appointment_status)""")

            conn.execute(query, {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'appointment_status': appointment_status
            })
    print("Dummy Appointment Data Inserted")


# -------- RECEPTION --------
def insert_reception(n=20000):
    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting Reception Data Please Wait.....!"):
            receptionist_name = fake.name()
            contact_no = generate_pak_number()

            query = text("""INSERT INTO reception (receptionist_name, contact_no) 
                             VALUES (:receptionist_name, :contact_no)""")

            conn.execute(query, {
                'receptionist_name': receptionist_name,
                'contact_no': contact_no
            })
    print("Dummy Receptionist Data Inserted")


# -------- DEPARTMENT --------
def insert_department(n=50):
    department_names = ['Anesthesia', 'Blood Bank', 'Oncology', 'Neonotology', 'Neurology', 'Plastic Surgery', 'Urology', 'Pathology', 'Radiology', 'General Surgery']
    hospital_locations = ['Block A', 'Block B', 'First Floor', 'Second Floor',
                         'Wing 1', 'Wing 2', 'North Wing', 'South Wing', 'Main Building', 'Annex']

    with engine.begin() as conn:
        for i in tqdm(range(n), desc="Inserting departments"):
            department_name = department_names[i % len(department_names)]
            department_location = hospital_locations[i % len(hospital_locations)]

            query = text("""
                INSERT INTO department (department_name, department_location)
                VALUES (:department_name, :department_location)
            """)
            conn.execute(query, {
                'department_name': department_name,
                'department_location': department_location
            })
    print("✅ Dummy departments inserted.")


# -------- LABARATORY --------
def insert_laboratory(n=1000000):
    test_names = ['Blood Test', 'X-Ray', 'MRI', 'CT Scan', 'Urine Test', 'COVID Test', 'ECG']
    test_results = ['Normal', 'Abnormal', 'Needs Follow-Up', 'Critical']

    with engine.begin() as conn:
        # Get existing patient and doctor IDs
        patient_ids = [row[0] for row in conn.execute(text("SELECT patient_id FROM patient")).fetchall()]
        doctor_ids = [row[0] for row in conn.execute(text("SELECT doctor_id FROM doctor")).fetchall()]

        if not patient_ids or not doctor_ids:
            print("No patients or doctors found! Insert them first.")
            return

        for _ in tqdm(range(n), desc="Inserting laboratory"):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            test_name = random.choice(test_names)
            test_date = fake.date_this_year()
            test_time = fake.time()
            test_result = random.choice(test_results)

            query = text("""
                INSERT INTO laboratory (patient_id, doctor_id, test_name, test_date, test_time, test_result)
                VALUES (:patient_id, :doctor_id, :test_name, :test_date, :test_time, :test_result)
            """)
            conn.execute(query, {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'test_name': test_name,
                'test_date': test_date,
                'test_time': test_time,
                'test_result': test_result
            })
    print("✅ Dummy laboratory records inserted.")


# -------- STAFF --------
def insert_staff(n=200):
    roles = ['Nurse', 'Cleaner', 'Security Guard', 'Ward Boy', 'Lab Assistant', 'Reception Support', 'Maintenance']

    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting staff"):
            first_name = fake.first_name()
            last_name = fake.last_name()
            role = random.choice(roles)
            contact_number = generate_pak_number()

            query = text("""
                INSERT INTO staff (first_name, last_name, staff_role, contact_number)
                VALUES (:first_name, :last_name, :role, :contact_number)
            """)
            conn.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'role': role,
                'contact_number': contact_number
            })
    print("✅ Dummy staff records inserted.")


# -------- PRESCRIPTION --------
def insert_prescriptions(n=1000000):
    procedures = ['Blood Pressure Monitoring', 'X-Ray Follow-up', 'General Checkup', 'MRI Scan', 'Medication Adjustment', 'Physical Therapy', 'Surgery Follow-up']

    with engine.begin() as conn:
        # Get existing patient and doctor IDs
        patient_ids = [row[0] for row in conn.execute(text("SELECT patient_id FROM patient")).fetchall()]
        doctor_ids = [row[0] for row in conn.execute(text("SELECT doctor_id FROM doctor")).fetchall()]

        if not patient_ids or not doctor_ids:
            print("No patients or doctors found! Insert them first.")
            return

        for _ in tqdm(range(n), desc="Inserting prescriptions"):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            procedure = random.choice(procedures)
            procedure_date = fake.date_this_year()
            next_appointment = fake.date_between(start_date=procedure_date)

            query = text("""
                INSERT INTO prescription (patient_id, doctor_id, patient_procedure, procedure_date, next_appointment)
                VALUES (:patient_id, :doctor_id, :procedure, :procedure_date, :next_appointment)
            """)
            conn.execute(query, {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'procedure': procedure,
                'procedure_date': procedure_date,
                'next_appointment': next_appointment
            })
    print("✅ Dummy prescription records inserted.")


# -------- ADMINISTRATOR --------
def insert_administrators(n=10):
    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting administrators"):
            first_name = fake.first_name()
            last_name = fake.last_name()
            contact_no = generate_pak_number()

            query = text("""
                INSERT INTO administrator (first_name, last_name, contact_no)
                VALUES (:first_name, :last_name, :contact_no)
            """)
            conn.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'contact_no': contact_no
            })
    print("✅ Dummy administrator records inserted.")


# -------- MEDICAL HISTORY --------
def insert_medical_history(n=1000000):
    diagnoses = [
        'Diabetes Type 2', 'Hypertension', 'Fracture', 'Migraine',
        'Pneumonia', 'Kidney Stones', 'Arthritis', 'Allergy',
        'Asthma', 'Heart Disease', 'Depression', 'COVID-19',
        'Tuberculosis', 'Hepatitis B', 'Thyroid Disorder', 'Gallstones',
        'Chronic Back Pain', 'Anemia', 'High Cholesterol', 'Skin Infection'
    ]

    treatments = [
        'Medication and diet control', 'Cast and rest', 'Antibiotics',
        'Pain management', 'Physical therapy', 'Surgery',
        'Regular checkups', 'Inhaler therapy', 'Cognitive Behavioral Therapy',
        'Vitamin supplements', 'Vaccination and isolation',
        'Blood transfusion', 'Dialysis', 'Laparoscopic surgery',
        'Topical creams', 'Cholesterol-lowering drugs',
        'Hormone therapy', 'Lifestyle modification', 'Mental health counseling',
        'Insulin therapy'
    ]

    with engine.begin() as conn:
        # Get existing patient and doctor IDs
        patient_ids = [row[0] for row in conn.execute(text("SELECT patient_id FROM patient")).fetchall()]
        doctor_ids = [row[0] for row in conn.execute(text("SELECT doctor_id FROM doctor")).fetchall()]

        if not patient_ids or not doctor_ids:
            print("No patients or doctors found! Insert them first.")
            return

        for _ in tqdm(range(n), desc="Inserting medical history"):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            diagnosis = random.choice(diagnoses)
            treatment_plan = random.choice(treatments)
            admission_date = fake.date_this_year()
            discharge_date = fake.date_between(start_date=admission_date)

            query = text("""
                INSERT INTO medical_history (patient_id, doctor_id, diagnosis, treatment_plan, admission_date, discharge_date)
                VALUES (:patient_id, :doctor_id, :diagnosis, :treatment_plan, :admission_date, :discharge_date)
            """)
            conn.execute(query, {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'diagnosis': diagnosis,
                'treatment_plan': treatment_plan,
                'admission_date': admission_date,
                'discharge_date': discharge_date
            })
    print("✅ Dummy medical history records inserted.")


# -------- MEDICINE --------
def insert_medicine(n=500000):
    medicines = [
        'Paracetamol', 'Ibuprofen', 'Aspirin', 'Amoxicillin', 'Metformin',
        'Lisinopril', 'Omeprazole', 'Simvastatin', 'Atorvastatin', 'Furosemide',
        'Prednisone', 'Insulin', 'Hydrochlorothiazide', 'Ciprofloxacin', 'Albuterol',
        'Clonazepam', 'Warfarin', 'Levothyroxine', 'Methotrexate', 'Diazepam'
    ]

    manufacturers = [
        'Pfizer', 'AstraZeneca', 'Novartis', 'Johnson & Johnson', 'Bayer',
        'Merck', 'Sanofi', 'GlaxoSmithKline', 'Roche', 'Eli Lilly'
    ]

    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting medicines"):
            medicine_name = random.choice(medicines)
            dosage = f'{random.randint(1, 250)} mg'
            manufacturer = random.choice(manufacturers)

            query = text("""
                INSERT INTO medicine (medicine_name, dosage, manufacturer)
                VALUES (:medicine_name, :dosage, :manufacturer)
            """)
            conn.execute(query, {
                'medicine_name': medicine_name,
                'dosage': dosage,
                'manufacturer': manufacturer
            })
    print("✅ Dummy medicine records inserted.")


# -------- SUPPLIER --------
def insert_suppliers(n=1000):
    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting suppliers"):
            supplier_name = fake.company()
            contact_no = generate_pak_number()
            email = fake.email()

            query = text("""
                INSERT INTO supplier (supplier_name, contact_no, email)
                VALUES (:supplier_name, :contact_no, :email)
            """)
            conn.execute(query, {
                'supplier_name': supplier_name,
                'contact_no': contact_no,
                'email': email
            })
    print("✅ Dummy supplier records inserted.")


# -------- ROOMS --------
def insert_room(n=50):
    room_types = ['Single', 'Double', 'ICU', 'General', 'VIP']

    with engine.begin() as conn:
        # Get existing patient IDs
        patient_ids = [row[0] for row in conn.execute(text("SELECT patient_id FROM patient")).fetchall()]

        if not patient_ids:
            print("No patients found! Insert them first.")
            return

        for _ in tqdm(range(n), desc="Inserting rooms"):
            patient_id = random.choice(patient_ids) if random.random() > 0.3 else None  # 30% chance of being vacant
            room_number = random.randint(101, 999)
            room_type = random.choice(room_types)
            status = 'Occupied' if patient_id else 'Vacant'

            query = text("""
                INSERT INTO room (patient_id, room_number, room_type, status)
                VALUES (:patient_id, :room_number, :room_type, :status)
            """)
            conn.execute(query, {
                'patient_id': patient_id,
                'room_number': room_number,
                'room_type': room_type,
                'status': status
            })
    print("✅ Dummy room records inserted.")


# -------- PAYMENT --------
def insert_payments(n=1000000):
    payment_statuses = ['Paid', 'Pending']

    with engine.begin() as conn:
        # Get existing patient IDs
        patient_ids = [row[0] for row in conn.execute(text("SELECT patient_id FROM patient")).fetchall()]

        if not patient_ids:
            print("No patients found! Insert them first.")
            return

        for _ in tqdm(range(n), desc="Inserting payments"):
            patient_id = random.choice(patient_ids)
            amount = round(random.uniform(100, 1000), 2)
            payment_status = random.choice(payment_statuses)

            query = text("""
                INSERT INTO payment (patient_id, amount, payment_status)
                VALUES (:patient_id, :amount, :payment_status)
            """)
            conn.execute(query, {
                'patient_id': patient_id,
                'amount': amount,
                'payment_status': payment_status
            })
    print("✅ Dummy payment records inserted.")


# # -------- PARKING --------
def insert_parkings(n=50000):
    vehicle_types = ['Car', 'Motorbike', 'Truck', 'Van', 'Bicycle']

    with engine.begin() as conn:
        for _ in tqdm(range(n), desc="Inserting parking records"):
            driver_name = fake.name()
            driver_contact = generate_pak_number(),
            vehicle_type = random.choice(vehicle_types)
            vehicle_no = f"{random.choice(['LE', 'ISB', 'KHI'])}-{random.randint(1000, 9999)}"
            exit_time = fake.time()

            query = text("""
                INSERT INTO parking (driver_name, driver_contact, vehicle_type, vehicle_no, exit_time)
                VALUES (:driver_name, :driver_contact, :vehicle_type, :vehicle_no, :exit_time)
            """)
            conn.execute(query, {
                'driver_name': driver_name,
                'driver_contact': driver_contact,
                'vehicle_type': vehicle_type,
                'vehicle_no': vehicle_no,
                'exit_time': exit_time
            })
    print("✅ Dummy parking records inserted.")

# -------- MAIN EXECUTION --------
if __name__ == "__main__":

    # Reset sequences 
    reset_sequences()


    # Execute all insert functions in the correct order
    insert_patient()
    insert_doctor()
    insert_appointment()
    insert_reception()
    insert_department()
    insert_laboratory()
    insert_staff()
    insert_administrators()
    insert_suppliers()
    insert_medicine()
    insert_prescriptions()
    insert_medical_history()
    insert_room()
    insert_payments()
    insert_parkings()


