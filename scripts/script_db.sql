CREATE DATABASE MELI_DB;

USE MELI_DB;

CREATE TABLE Proccesors
(
	Proccesor_ID int not null auto_increment,
    	Brand varchar(255) not null,
    	Vendor varchar(255) not null,
    	Speed varchar(20) not null,
    	PRIMARY KEY(Proccesor_ID)
);

CREATE TABLE OS 
(
	OS_ID int not null auto_increment,
    	OS_Name varchar(255) not null,
    	OS_Node varchar(255) not null,
    	OS_Version varchar(255) not null,
	PRIMARY KEY (OS_ID)
);

CREATE TABLE Servers
(
	Server_ID int not null auto_increment,
    	OS_ID int not null,
    	Proccesor_ID int not null,
    	IP varchar(50) not null,
    	PRIMARY KEY(Server_ID),
    	FOREIGN KEY(OS_ID) REFERENCES OS(OS_ID),
    	FOREIGN KEY(Proccesor_ID) REFERENCES Proccesors(Proccesor_ID)
);

CREATE TABLE Executions
(
	Exec_ID int not null auto_increment,
	Server_ID int not null,
	Exec_date datetime not null,
    	PRIMARY KEY (Exec_ID),
    	FOREIGN KEY (Server_ID) REFERENCES Servers(Server_ID)
);

CREATE TABLE Processes
(
	PID int not null,
    	Process_Name varchar(255) not null,
    	PRIMARY KEY(PID)
);

CREATE TABLE USERS
(
	User_ID int not null auto_increment,
	User_Name varchar(255) not null,
    	PRIMARY KEY(User_ID)
);

CREATE TABLE USERS_PER_EXECUTION
(
	Execution_ID int not null,
    	User_ID int not null,
	FOREIGN KEY(Execution_ID) REFERENCES Executions(Exec_ID),
    	FOREIGN KEY(User_ID) REFERENCES USERS(User_ID)
);

CREATE TABLE PROCESSES_PER_EXECUTION
(
	Execution_ID int not null,
    	PID int not null,
	FOREIGN KEY(Execution_ID) REFERENCES Executions(Exec_ID),
    	FOREIGN KEY(PID) REFERENCES Processes(PID)
);


DELIMITER $$
CREATE PROCEDURE insert_os_data(system_name varchar(255), system_node varchar(255), system_version varchar(255))
BEGIN
	IF NOT EXISTS(SELECT 1 FROM MELI_DB.OS WHERE OS_Name = system_name and OS_Node = system_node and OS_Version = system_version) THEN		
		insert into MELI_DB.OS (OS_Name, OS_Node, OS_Version) values (system_name, system_node, system_version);
	END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_proccesor_data(brand varchar(255), vendor varchar(255), speed varchar(255))
BEGIN
	IF NOT EXISTS(SELECT 1 FROM MELI_DB.Proccesors P WHERE
    	P.Brand = brand and P.Vendor = vendor and P.Speed = speed) THEN
		insert into MELI_DB.Proccesors (Brand, Vendor, speed) values (brand, vendor, speed);
	END IF;        
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_servers_data
(
fecha_ejecucion datetime, ip varchar(50),brand varchar(255), vendor varchar(255), speed varchar(255),
system_name varchar(255), system_node varchar(255), system_version varchar(255)
)
BEGIN
    
	set @OS_Id = (select OS_ID from MELI_DB.OS where OS_Name = system_name and OS_Node = system_node and OS_Version = system_version);
	set @Proccesor_Id = (select Proccesor_ID from MELI_DB.Proccesors where Brand = brand and Vendor = vendor and Speed = speed);
		
	/*Aca es mas facil porqe nunca va a haber 2 IPS iguales*/

	if not exists(select 1 from MELI_DB.Servers where IP = ip) then
		insert into MELI_DB.Servers (OS_ID, Proccesor_ID, IP) values (@OS_Id, @Proccesor_ID, ip);
	end if;
    
    	set @server_id = (select Server_ID from MELI_DB.Servers where IP = ip);
    
    	insert into MELI_DB.Executions (Server_ID, Exec_date) values (@server_id, fecha_ejecucion);
    
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_processes_data(fecha_ejecucion datetime, p_id int, p_name varchar(255))
BEGIN
	if not exists(select 1 from MELI_DB.Processes where PID = p_id and Process_Name = p_name ) then
    		insert into MELI_DB.Processes (PID, Process_Name) values (p_id, p_name);
	end if;
    
    	set @exec_id = (select Exec_ID from MELI_DB.Executions where Exec_date = fecha_ejecucion);
    	insert into MELI_DB.PROCESSES_PER_EXECUTION (Execution_ID, PID) values (@exec_id, p_id);
    
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_users_data(fecha_ejecucion datetime, username varchar(255))
BEGIN
	if not exists (select 1 from MELI_DB.USERS where User_Name = username) then
		insert into MELI_DB.USERS (User_Name) values (username);
	end if;
    
	set @exec_id = (select Exec_ID from MELI_DB.Executions where Exec_date = fecha_ejecucion);
    	set @user_id = (select User_ID from MELI_DB.USERS where User_Name = username);
    
    	insert into MELI_DB.USERS_PER_EXECUTION (Execution_ID, User_ID) values (@exec_id, @user_id);
    
END$$
DELIMITER ;