1) Doctor

CREATE OR REPLACE FUNCTION delete_doc() 
RETURNS TRIGGER 
AS $$
BEGIN
	DELETE FROM prescribes WHERE prescribes.doc_id = OLD.doc_id;
	DELETE FROM undergoes WHERE undergoes.doc_id = OLD.doc_id;
	DELETE FROM department WHERE department.head_id = OLD.doc_id;
    DELETE FROM appointment WHERE appointment.doc_id = OLD.doc_id;  
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER doc
BEFORE DELETE ON doctor
FOR EACH ROW
EXECUTE FUNCTION delete_doc();

2) Patient

CREATE OR REPLACE FUNCTION delete_pat() 
RETURNS TRIGGER 
AS $$
BEGIN
	DELETE FROM prescribes WHERE prescribes.pat_id = OLD.pat_id;
	DELETE FROM undergoes WHERE undergoes.pat_id = OLD.pat_id;
    DELETE FROM appointment WHERE appointment.pat_id = OLD.pat_id;  
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pat
BEFORE DELETE ON patient
FOR EACH ROW
EXECUTE FUNCTION delete_pat();



3) Appointment

CREATE OR REPLACE FUNCTION delete_app() 
RETURNS TRIGGER 
AS $$
BEGIN
	DELETE FROM prescribes WHERE prescribes.app_id = OLD.app_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER app
BEFORE DELETE ON appointment
FOR EACH ROW
EXECUTE FUNCTION delete_app();


4) Undergoes

CREATE OR REPLACE FUNCTION check_availability() 
RETURNS TRIGGER 
AS $$
DECLARE
    a INTEGER;
    b INTEGER;
BEGIN
    SELECT COUNT(under_id) INTO a FROM undergoes WHERE room_no = NEW.room_no;
    SELECT available INTO b FROM room WHERE room_no = NEW.room_no;
    IF a > b THEN
        DELETE FROM undergoes WHERE under_id = NEW.under_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER avroom 
AFTER INSERT ON undergoes 
FOR EACH ROW
EXECUTE FUNCTION check_availability();



5) Nurse

CREATE OR REPLACE FUNCTION delete_nur() 
RETURNS TRIGGER 
AS $$
BEGIN
	DELETE FROM undergoes WHERE undergoes.nur_id = OLD.nur_id;  
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER nur
BEFORE DELETE ON nurse
FOR EACH ROW
EXECUTE FUNCTION delete_nur();







1) Patients

CREATE OR REPLACE PROCEDURE count_patients(OUT patient_count INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
    SELECT COUNT(*) INTO patient_count FROM patient;
END;
$$;

2) Doctors

CREATE OR REPLACE PROCEDURE count_doctors(OUT doctor_count INTEGER) 
LANGUAGE plpgsql AS $$
BEGIN
    SELECT COUNT(*) INTO doctor_count FROM doctor;
END;
$$;

3) Nurses

CREATE OR REPLACE PROCEDURE count_nurses(OUT nurse_count INTEGER) 
LANGUAGE plpgsql AS $$
BEGIN
    SELECT COUNT(*) INTO nurse_count FROM nurse;
END;
$$;

4) Appointment

CREATE OR REPLACE PROCEDURE count_appointments(OUT appointment_count INTEGER) 
LANGUAGE plpgsql AS $$
BEGIN
    SELECT COUNT(*) INTO appointment_count FROM appointment;
END;
$$;

5) Rooms

CREATE OR REPLACE PROCEDURE count_rooms(OUT room_count INTEGER) 
LANGUAGE plpgsql AS $$
BEGIN
    SELECT COUNT(*) INTO room_count FROM room;
END;
$$;

6) Medications

CREATE OR REPLACE FUNCTION count_medications() RETURNS INTEGER AS $$
DECLARE
    medication_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO medication_count FROM medication;
    RETURN medication_count;
END;
$$ LANGUAGE plpgsql;

7) Department

CREATE OR REPLACE FUNCTION count_departments() RETURNS INTEGER AS $$
DECLARE
    department_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO department_count FROM department;
    RETURN department_count;
END;
$$ LANGUAGE plpgsql;

8) Procedure

CREATE OR REPLACE FUNCTION count_procedures() RETURNS INTEGER AS $$
DECLARE
    procedure_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO procedure_count FROM procedure;
    RETURN procedure_count;
END;
$$ LANGUAGE plpgsql;

9) Undergoes

CREATE OR REPLACE FUNCTION count_undergoes() RETURNS INTEGER AS $$
DECLARE
    undergoes_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO undergoes_count FROM undergoes;
    RETURN undergoes_count;
END;
$$ LANGUAGE plpgsql;

10) Prescribes

CREATE OR REPLACE FUNCTION count_prescribes() RETURNS INTEGER AS $$
DECLARE
    prescribes_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO prescribes_count FROM prescribes;
    RETURN prescribes_count;
END;
$$ LANGUAGE plpgsql;


CALL count_patients(NULL);
CALL count_doctors(NULL);
CALL count_nurses(NULL);
CALL count_appointments(NULL);
CALL count_rooms(NULL);
Select count_medications();
Select count_departments();
Select count_procedures();
Select count_undergoes();
Select count_prescribes();















