select Server_ID, IP, Exec_date, (select count(*) from PROCESSES_PER_EXECUTION PPE  where PPE.Execution_ID = E.Exec_ID) as 'Cantidad de Procesos Ejecutando' from Executions E join Servers S on E.Server_ID = S.Server_ID ;