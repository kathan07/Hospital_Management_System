CREATE OR REPLACE TRIGGER doc BEFORE DELETE ON doctor
FOR EACH ROW
BEGIN
    DELETE FROM appointment WHERE appointment.doc_id = :old.doc_id;
    DELETE FROM department WHERE department.head_id = :old.doc_id;
    DELETE FROM undergoes WHERE undergoes.doc_id = :old.doc_id;
    DELETE FROM prescribes WHERE prescribes.doc_id = :old.doc_id;
END;
/

CREATE OR REPLACE TRIGGER pat BEFORE DELETE ON patient
FOR EACH ROW
BEGIN
    DELETE FROM appointment WHERE appointment.doc_id = :old.doc_id;
    DELETE FROM undergoes WHERE undergoes.doc_id = :old.doc_id;
    DELETE FROM prescribes WHERE prescribes.doc_id = :old.doc_id;
END;
/


CREATE OR REPLACE TRIGGER avroom AFTER INSERT ON undergoes
FOR EACH ROW
    a NUMBER;
    b NUMBER;
BEGIN
    SELECT COUNT(under_id) INTO a FROM undergoes WHERE room_no =:new.room_no;
    SELECT availabe INTO b FROM room WHERE room_no =:new.room_no;
    IF a>b THEN
        DELETE FROM undergoes WHERE under_id =:new.under_id;
    END IF;
END;
/