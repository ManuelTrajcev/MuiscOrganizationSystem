CREATE TABLE PersonalInfo (
    personal_info_id SERIAL PRIMARY KEY,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postalcode TEXT,
    phone TEXT,
    fax TEXT,
    email TEXT
);

ALTER TABLE employee
ADD COLUMN personal_info_id INTEGER REFERENCES PersonalInfo(personal_info_id);

ALTER TABLE customer
ADD COLUMN personal_info_id INTEGER REFERENCES PersonalInfo(personal_info_id);

--PERSONAL INFO DATA MIGRATION
INSERT INTO PersonalInfo (address, city, state, country, postalcode, phone, fax, email)
SELECT DISTINCT address, city, state, country, postal_code, phone, fax, email
FROM employee;

UPDATE employee e
SET personal_info_id = p.personal_info_id
FROM PersonalInfo p
WHERE e.address = p.address
  AND e.city = p.city
  AND e.state = p.state
  AND e.country = p.country
  AND e.postal_code = p.postalcode
  AND e.phone = p.phone
  AND e.fax = p.fax
  AND e.email = p.email;

INSERT INTO PersonalInfo (address, city, state, country, postalcode, phone, fax, email)
SELECT DISTINCT address, city, state, country, postal_code, phone, fax, email
FROM customer;

UPDATE customer c
SET personal_info_id = p.personal_info_id
FROM PersonalInfo p
WHERE c.address = p.address
  AND c.city = p.city
  AND c.country = p.country
  AND c.email = p.email;


ALTER TABLE employee
DROP COLUMN address,
DROP COLUMN city,
DROP COLUMN state,
DROP COLUMN country,
DROP COLUMN postal_code,
DROP COLUMN phone,
DROP COLUMN fax,
DROP COLUMN email;

ALTER TABLE customer
DROP COLUMN address,
DROP COLUMN city,
DROP COLUMN state,
DROP COLUMN country,
DROP COLUMN postal_code,
DROP COLUMN phone,
DROP COLUMN fax,
DROP COLUMN email;

ALTER TABLE personalinfo
RENAME COLUMN postalcode TO postal_code;

SELECT *
FROM employee

CREATE TABLE Contact (
    contact_id INT PRIMARY KEY,
    phone VARCHAR(50),
    fax VARCHAR(50),
    email VARCHAR(100)
);

INSERT INTO Contact (contact_id, phone, fax, email)
SELECT
    personal_info_id,
    Phone,
    Fax,
    Email
FROM personalinfo;

ALTER TABLE Employee
ADD contact_id INT;

UPDATE Employee
SET contact_id = employee.personal_info_id
where employee.personal_info_id IS NOT  NULL;

ALTER TABLE Employee
ADD CONSTRAINT FK_Employee_Contact FOREIGN KEY (contact_id)
REFERENCES Contact(contact_id);

ALTER TABLE Customer
ADD contact_id INT;

UPDATE Customer
SET contact_id = customer.personal_info_id
where customer.personal_info_id IS NOT  NULL;

ALTER TABLE Customer
ADD CONSTRAINT FK_Customer_Contact FOREIGN KEY (contact_id)
REFERENCES Contact(contact_id);

ALTER TABLE personalinfo
DROP COLUMN fax,
DROP COLUMN phone,
DROP COLUMN email;

ALTER TABLE personalinfo RENAME TO address_info;
