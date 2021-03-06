CREATE TABLE Proccesors
(
	Proccesor_ID int not null auto_increment,
    	Brand varchar(255) not null,
    	Vendor varchar(255) not null,
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
	Indice int not null auto_increment, 	/*Utilizo un INDICE como PK ya que puede darse la situacion en donde hay 2 procesos con mismo PID (en SO diferentes) y nombre distintos*/
	PID int not null,
    	Process_Name varchar(255) not null,
    	PRIMARY KEY(Indice)
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
    	Indice_P int not null,
	FOREIGN KEY(Execution_ID) REFERENCES Executions(Exec_ID),
    	FOREIGN KEY(Indice_P) REFERENCES Processes(Indice)
);


DELIMITER $$
CREATE PROCEDURE insert_os_data(system_name varchar(255), system_node varchar(255), system_version varchar(255))
BEGIN
	IF NOT EXISTS(SELECT 1 FROM OS WHERE OS_Name = system_name and OS_Node = system_node and OS_Version = system_version) THEN		
		insert into OS (OS_Name, OS_Node, OS_Version) values (system_name, system_node, system_version);
	END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_proccesor_data(brand varchar(255), vendor varchar(255))
BEGIN
	IF NOT EXISTS(SELECT 1 FROM Proccesors P WHERE P.Brand = brand and P.Vendor = vendor) THEN
		insert into Proccesors (Brand, Vendor) values (brand, vendor);
	END IF;        
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_servers_data
(
fecha_ejecucion datetime, ip varchar(50),brand varchar(255), vendor varchar(255),
system_name varchar(255), system_node varchar(255), system_version varchar(255)
)
BEGIN
    
	set @OS_Id = (select OS_ID from OS O where O.OS_Name = system_name and O.OS_Node = system_node and O.OS_Version = system_version);
	set @Proccesor_Id = (select Proccesor_ID from Proccesors P where P.Brand = brand and P.Vendor = vendor);
		
	/*Aca es mas facil porqe nunca va a haber 2 IPS iguales*/

	if not exists(select 1 from Servers S where S.IP = ip) then
		insert into Servers (OS_ID, Proccesor_ID, IP) values (@OS_Id, @Proccesor_ID, ip);
	end if;
    
    	set @server_id = (select Server_ID from Servers S where S.IP = ip);
    
    	insert into Executions (Server_ID, Exec_date) values (@server_id, fecha_ejecucion);
    
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_processes_data(fecha_ejecucion datetime, p_id int, p_name varchar(255))
BEGIN
	if not exists(select 1 from Processes where PID = p_id and Process_Name = p_name ) then
    		insert into Processes (PID, Process_Name) values (p_id, p_name);
	end if;
    
    	set @exec_id = (select Exec_ID from Executions E where E.Exec_date = fecha_ejecucion);
	set @indice_p = (select Indice from Processes P where P.PID = p_id and P.Process_Name = p_name);

    	insert into PROCESSES_PER_EXECUTION (Execution_ID, Indice_P) values (@exec_id, @indice_p);    
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE insert_users_data(fecha_ejecucion datetime, username varchar(255))
BEGIN
	if not exists (select 1 from USERS U where U.User_Name = username) then
		insert into USERS (User_Name) values (username);
	end if;
    
	set @exec_id = (select Exec_ID from Executions E where E.Exec_date = fecha_ejecucion);
    	set @user_id = (select User_ID from USERS U where U.User_Name = username);
    
    	insert into USERS_PER_EXECUTION (Execution_ID, User_ID) values (@exec_id, @user_id);
    
END$$
DELIMITER ;