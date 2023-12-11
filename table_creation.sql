	-- create tables for book fetch database
	CREATE DATABASE if not exists cisc450project;
	USE cisc450project;

	CREATE TABLE super_administrator(
		sa_admin_employeeID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		sa_first_name VARCHAR(20) NOT NULL, 
		sa_last_name VARCHAR(35) NOT NULL,
		gender VARCHAR(10), 
		salary DECIMAL(12,2) NOT NULL, 
		ssn VARCHAR(11) NOT NULL CHECK(ssn REGEXP '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'), 
		email VARCHAR(20) NOT NULL CHECK(email LIKE "%@%"), 
		address VARCHAR(100), 
		phone_number VARCHAR(12) NOT NULL CHECK(phone_number REGEXP '^[0-9]{10}$')
	);

	CREATE TABLE customer_support(
		employeeID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		cs_first_name VARCHAR(20) NOT NULL, 
		cs_last_name VARCHAR(30), 
		gender VARCHAR(10), 
		salary DECIMAL(12,2), 
		ssn VARCHAR(11) CHECK(ssn REGEXP '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'), 
		email VARCHAR(20) CHECK(email LIKE '%@%'), 
		address VARCHAR(100), 
		phone_number VARCHAR(12) CHECK(phone_number REGEXP '^[0-9]{10}$'), 
		sa_admin_employeeID MEDIUMINT UNSIGNED,
		foreign key (sa_admin_employeeID) references super_administrator(sa_admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE administrator(
		admin_employeeID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
		admin_first_name VARCHAR(20) NOT NULL, 
		admin_last_name VARCHAR(35),
		gender VARCHAR(10), 
		salary DECIMAL(12,2), 
		ssn VARCHAR(11) CHECK(ssn REGEXP '^[0-9]{3}-[0-9]{2}-[0-9]{4}$'), 
		email VARCHAR(20) CHECK(email LIKE '%@%'), 
		address VARCHAR(100), 
		phone_number VARCHAR(12) CHECK(phone_number REGEXP '^[0-9]{10}$'),
		sa_admin_employeeID MEDIUMINT UNSIGNED,
		foreign key (sa_admin_employeeID) references super_administrator(sa_admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE 
	);

	CREATE TABLE trouble_ticket(
		ticketID INT UNSIGNED AUTO_INCREMENT, 
		trouble_category VARCHAR(15) CHECK(trouble_category IN('userprofile', 'products', 'cart', 'orders', 'others')), 
		date_logged DATE, 
		date_completed DATE,
		ticket_title VARCHAR(100) NOT NULL,
		prob_desc VARCHAR(500), 
		fixed_desc VARCHAR(500), 
		status VARCHAR(20) NOT NULL CHECK(status IN('new', 'assigned', 'in-process', 'completed')), 
		cs_employeeID MEDIUMINT UNSIGNED, 
		a_employeeID MEDIUMINT UNSIGNED, 
		studentID INT UNSIGNED,
		PRIMARY KEY (ticketID, status),
		foreign key (cs_employeeID) references customer_support(employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (a_employeeID) references administrator(admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE investigates(
		employeeID MEDIUMINT UNSIGNED, 
		ticketID INT UNSIGNED,
		PRIMARY KEY(employeeID, ticketID),
		foreign key (employeeID) references customer_support(employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (ticketID) references trouble_ticket(ticketID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);


	CREATE TABLE department(
		departmentID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		dep_name VARCHAR(100) NOT NULL, 
		admin_employeeID MEDIUMINT UNSIGNED, 
		foreign key (admin_employeeID) references administrator(admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE university(
		universityID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		university_name VARCHAR(100) NOT NULL, 
		address VARCHAR(100), 
		rep_first_name VARCHAR(25), 
		rep_last_name VARCHAR(35), 
		rep_email VARCHAR(40) CHECK (rep_email LIKE "%@%"), 
		rep_phone VARCHAR(12) CHECK(rep_phone REGEXP '^[0-9]{10}$'), 
		admin_employeeID MEDIUMINT UNSIGNED,
		FOREIGN KEY (admin_employeeID) REFERENCES administrator(admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE university_department(
		universityID MEDIUMINT UNSIGNED, 
		departmentID MEDIUMINT UNSIGNED,
		PRIMARY KEY (universityID, departmentID),
		FOREIGN KEY (universityID) REFERENCES university(universityID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		FOREIGN KEY (departmentID) REFERENCES department(departmentID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE instructor(
		instructorID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		first_name VARCHAR(25) NOT NULL, 
		last_name VARCHAR(35) NOT NULL, 
		universityID MEDIUMINT UNSIGNED NOT NULL, 
		departmentID MEDIUMINT UNSIGNED, 
		FOREIGN KEY (universityID) REFERENCES university(universityID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		FOREIGN KEY (departmentID) REFERENCES department(departmentID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE student(
		studentID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,  
		student_first_name VARCHAR(25) NOT NULL,  
		student_last_name VARCHAR(25) NOT NULL, 
		email VARCHAR(60) NOT NULL,  
		address VARCHAR(50), 
		phone VARCHAR(12) CHECK (phone REGEXP '^[0-9]{10}$'),
		birthdate DATE CHECK(birthdate > "1960-01-01"),
		major VARCHAR(20),
		student_status VARCHAR(15) CHECK(student_status = 'Grad' OR student_status = 'UnderGrad'),  
		year TINYINT,  
		universityID MEDIUMINT UNSIGNED NOT NULL, 
		FOREIGN KEY (universityID) REFERENCES university(universityID) 
			ON UPDATE CASCADE
			ON DELETE CASCADE 
	); 

	CREATE TABLE course(
		courseID SMALLINT UNSIGNED PRIMARY KEY,  
		course_name VARCHAR(50) NOT NULL,  
		year SMALLINT CHECK(year REGEXP '20[0-9]{2}'),  
		semester_offered VARCHAR(10),  
		departmentID MEDIUMINT UNSIGNED,
		instructorID MEDIUMINT UNSIGNED,  
		admin_employeeID MEDIUMINT UNSIGNED,  
		FOREIGN KEY (departmentID) REFERENCES department(departmentID) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		FOREIGN KEY (instructorID) references instructor(instructorID) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		FOREIGN KEY (admin_employeeID) references administrator(admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	); 

	CREATE TABLE takes(
		courseID SMALLINT UNSIGNED, 
		studentID MEDIUMINT UNSIGNED, 
		PRIMARY KEY(courseID, studentID),
		FOREIGN KEY (courseID) REFERENCES course(courseID) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE, 
		FOREIGN KEY (studentID) REFERENCES student(studentID) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE 
	); 

	CREATE TABLE book(
		isbn INT UNSIGNED PRIMARY KEY, 
		book_type VARCHAR(50) CHECK(book_type IN("new", "used")), 
		price DECIMAL(5,2), 
		book_title VARCHAR(200) NOT NULL, 
		ISBN13 INT UNSIGNED, 
		publisher VARCHAR(50), 
		published_date DATE, 
		edition SMALLINT UNSIGNED, 
		language VARCHAR(50), 
		format VARCHAR(10) CHECK(format IN("hardcover", "soft", "electronic")) , 
		category VARCHAR(30), 
		subcategory VARCHAR(30), 
		average_rating DECIMAL(2,1) CHECK(average_rating BETWEEN 0.0 AND 5.0), 
		admin_employeeID MEDIUMINT UNSIGNED,
		foreign key (admin_employeeID) references administrator(admin_employeeID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE author(
		isbn INT UNSIGNED,
		author_name VARCHAR(100),
		PRIMARY KEY(isbn, author_name),
		foreign key (isbn) references book(isbn)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE course_books(
		courseID SMALLINT UNSIGNED, 
		isbn INT UNSIGNED, 
		FOREIGN KEY (courseID) REFERENCES course(courseID) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE, 
		FOREIGN KEY (isbn) REFERENCES book(isbn) 
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	); 

	CREATE TABLE recommendation(
		isbn INT UNSIGNED,
		studentID MEDIUMINT UNSIGNED,
		PRIMARY KEY (isbn, studentID),
		foreign key (isbn) references book(isbn)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (studentID) references student(studentID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE book_keyword(
		isbn INT UNSIGNED, 
		keyword_description VARCHAR(200),
		PRIMARY KEY(isbn, keyword_description),
		foreign key (isbn) references book(isbn)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
		);

	CREATE TABLE cart(
		cartID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		total_cost DECIMAL(8,2), 
		date_created DATE, 
		date_updated DATE, 
		studentID MEDIUMINT UNSIGNED NOT NULL,
		foreign key (studentID) references student(studentID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE add_book(
		isbn INT UNSIGNED NOT NULL,
		cartID INT UNSIGNED NOT NULL, 
		quantity SMALLINT UNSIGNED NOT NULL, 
		purchase_type VARCHAR(5) NOT NULL CHECK(purchase_type IN("rent", "buy")),
		PRIMARY KEY(isbn, cartID),
		foreign key (isbn) references book(isbn)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (cartID) references cart(cartID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE credit_card(
		credit_cardID MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		credit_card_number BIGINT UNSIGNED NOT NULL,
		credit_card_name VARCHAR(100) NOT NULL, 
		credit_card_expiration DATE NOT NULL, 
		credit_card_type VARCHAR(50) NOT NULL
	);

	CREATE TABLE final_order(
		orderID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		cartID INT UNSIGNED, 
		date_created DATE, 
		date_completed DATE, 
		status VARCHAR(20) NOT NULL CHECK(status IN('new', 'processed','shipping', 'shipped','canceled')), 
		ship_type VARCHAR(10) NOT NULL CHECK(ship_type IN('standard', '2-day', '1-day')), 
		ship_address VARCHAR(100), 
		credit_cardID MEDIUMINT UNSIGNED NOT NULL,
		CHECK(date_completed >= date_created),
		foreign key (cartID) references cart(cartID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (credit_cardID) references credit_card(credit_cardID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);

	CREATE TABLE review(
		reviewID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, 
		orderID INT UNSIGNED, 
		rating DECIMAL(2,1) NOT NULL CHECK(rating BETWEEN 0 AND 5), 
		comment VARCHAR(500), 
		date_submitted DATE, 
		isbn INT UNSIGNED NOT NULL, 
		studentID MEDIUMINT UNSIGNED NOT NULL,
		foreign key (studentID) references student(studentID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (orderID) references final_order(orderID)
			ON UPDATE CASCADE 
			ON DELETE CASCADE,
		foreign key (isbn) references book(isbn)
			ON UPDATE CASCADE 
			ON DELETE CASCADE
	);






