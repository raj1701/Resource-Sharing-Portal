Data Base Name = DBMS_Notes_Portal

Database User - name = DBMS_user
	      -	password = Dbmsproject


mysql> desc Department;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| DeptNo     | int(11)     | NO   | PRI | NULL    |       |
| DeptName   | varchar(50) | NO   |     | NULL    |       |
| DeptInfo   | text        | NO   |     | NULL    |       |
| NoOfCouses | int(11)     | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
4 rows in set (0.02 sec)

