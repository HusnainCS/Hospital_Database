-- ===============================
-- Hospital Management System SQL Schema
-- ===============================

-- ===============================
-- 1. Patient Table
-- ===============================
CREATE TABLE patient (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    contact_number VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 2. Doctor Table
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
-- 3. Appointment Table
-- ===============================
CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    appointment_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 4. Receptionist Table
-- ===============================
CREATE TABLE reception (
    receptionist_id SERIAL PRIMARY KEY,
    receptionist_name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 5. Department Table
-- ===============================
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_location VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 6. Laboratory Table
-- ===============================
CREATE TABLE laboratory (
    test_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    test_name VARCHAR(100),
    test_date DATE NOT NULL,
    test_time TIME NOT NULL,
    test_result VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 7. Staff Table
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
-- 8. Prescription Table
-- ===============================
CREATE TABLE prescription (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    patient_procedure VARCHAR(400) NOT NULL,
    procedure_date DATE NOT NULL,
    next_appointment DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 9. Administrator Table
-- ===============================
CREATE TABLE administrator (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    contact_no VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 10. Medical History Table
-- ===============================
CREATE TABLE medical_history (
    record_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    doctor_id INT NOT NULL REFERENCES doctor(doctor_id),
    diagnosis VARCHAR(500) NOT NULL,
    treatment_plan VARCHAR(200) NOT NULL,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 11. Medicine Table
-- ===============================
CREATE TABLE medicine (
    medicine_id SERIAL PRIMARY KEY,
    medicine_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    manufacturer VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 12. Supplier Table
-- ===============================
CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_no VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 13. Room Table
-- ===============================
CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    room_number INT NOT NULL,
    room_type VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 14. Payment Table
-- ===============================
CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL REFERENCES patient(patient_id),
    amount DECIMAL(10, 2),
    payment_status VARCHAR(10) CHECK (payment_status IN ('Paid', 'Pending')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- 15. Parking Table
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
