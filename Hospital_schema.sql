

-- ===============================
-- 1. Patient Table (base table)
-- ===============================
CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age VARCHAR(3),
    date_of_birth DATE,
    gender VARCHAR(10),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 2. Doctor Table (base table)
-- ===============================
CREATE TABLE doctor (
    doctor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    speciality VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    contact_no VARCHAR(15),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 3. Department Table (base table)
-- ===============================
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_location VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 4. Medicine Table (base table)
-- ===============================
CREATE TABLE medicine (
    medicine_id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    manufacturer VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 5. Supplier Table (base table)
-- ===============================
CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Now create tables with foreign key dependencies

-- ===============================
-- 6. Appointment Table (depends on patient and doctor)
-- ===============================
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_doctor
        FOREIGN KEY(doctor_id) 
        REFERENCES doctor(doctor_id)
);

-- ===============================
-- 7. Medical History Table (depends on patient and doctor)
-- ===============================
CREATE TABLE medical_history (
    record_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    diagnosis VARCHAR(500) NOT NULL,
    treatment_plan VARCHAR(200) NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_medical_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id),
    CONSTRAINT fk_medical_doctor
        FOREIGN KEY(doctor_id) 
        REFERENCES doctor(doctor_id)
);

-- ===============================
-- 8. Prescription Table (depends on patient and doctor)
-- ===============================
CREATE TABLE prescription (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    patient_procedure VARCHAR(400) NOT NULL,
    procedure_date DATE NOT NULL,
    next_appointment DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_prescription_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id),
    CONSTRAINT fk_prescription_doctor
        FOREIGN KEY(doctor_id) 
        REFERENCES doctor(doctor_id)
);

-- ===============================
-- 9. Laboratory Table (depends on patient and doctor)
-- ===============================
CREATE TABLE laboratory (
    test_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    test_name VARCHAR(100),
    test_date DATE NOT NULL,
    test_time TIME NOT NULL,
    test_result VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_lab_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id),
    CONSTRAINT fk_lab_doctor
        FOREIGN KEY(doctor_id) 
        REFERENCES doctor(doctor_id)
);

-- ===============================
-- 10. Room Table (depends on patient)
-- ===============================
CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    room_number INT NOT NULL,
    room_type VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_room_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id)
);

-- ===============================
-- 11. Payment Table (depends on patient)
-- ===============================
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    amount DECIMAL(10, 2),
    payment_status VARCHAR(10) CHECK (payment_status IN ('Paid', 'Pending')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_patient
        FOREIGN KEY(patient_id) 
        REFERENCES patient(patient_id)
);

-- ===============================
-- 12. Staff Table (independent)
-- ===============================
CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    staff_role VARCHAR(100) NOT NULL,
    contact_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 13. Receptionist Table (independent)
-- ===============================
CREATE TABLE reception (
    receptionist_id SERIAL PRIMARY KEY,
    receptionist_name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 14. Administrator Table (independent)
-- ===============================
CREATE TABLE administrator (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    contact_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 15. Parking Table (independent)
-- ===============================
CREATE TABLE parking (
    driver_id SERIAL PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    driver_contact VARCHAR(15) NOT NULL,
    vehicle_type VARCHAR(50),
    vehicle_no VARCHAR(20),
    exit_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


