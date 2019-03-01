#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  crudwrapper.py
#  
#  Copyright 2019 Coelodonta
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

class MYSQLPythonWrapperGenerator:
	
	def indent(self,out,n=1):
		for i in range(n):
			out.write("\t")
	
	def	processTable(self,out,tableName):
		out.write("\n# CRUD for table: "+tableName)
		out.write("\nclass "+tableName+"_CRUD:\n")
		self.indent(out)
		out.write("cnx=None\n\n")
		self.indent(out)
		out.write("def dbconnect(self, myhost, myuser, mypass, mydbname):\n")
		self.indent(out,2)
		out.write("self.cnx = pymysql.connect(user=myuser, password=mypass,host=myhost,database=mydbname)\n\n")
		self.indent(out)
		out.write("def close(self):\n")
		self.indent(out,2)
		out.write("self.cnx.close()\n\n")
		

	def	finishTable(self,out):
		out.write("\n")

	def processProcedure(self,out,procName,args):
		# Strip open/close parentheses
		args=args[1:-1]
		
		self.indent(out)
		# Function Signature
		out.write("def "+procName+"CRUD(self");

		if len(args):
			parms=[x.strip() for x in args.split(',')]
			parms=map(lambda x: x.split(' ') , parms)
			delim=", "
			for parm in parms:
				out.write(delim)
				out.write(parm[1])
				
		out.write("):\n")
		
		# Function Body
		self.indent(out,2)
		out.write("sql=\"CALL "+procName+"(") 
		if len(args):
			argLen=len(args.split(","))
			delim="%s"
			for i in range(argLen):
				out.write(delim)
				delim=", %s"
				
		out.write(")\";\n")

		self.indent(out,2)
		out.write("cursor = self.cnx.cursor(pymysql.cursors.DictCursor)\n")
		
		if len(args) < 1:
			self.indent(out,2)
			out.write("cursor.execute(sql)\n")
			
		else:
			self.indent(out,2)
			out.write("cursor.execute(sql,(")
			parms=[x.strip() for x in args.split(',')]
			parms=map(lambda x: x.split(' ') , parms)
			delim=""
			for parm in parms:
				out.write(delim)
				out.write(parm[1])
				delim=","
				
			out.write("))\n")

		if "SelectOne" in procName:
			self.indent(out,2)
			out.write("result=cursor.fetchall()\n")
			self.indent(out,2)
			out.write("cursor.close()\n")
			self.indent(out,2)
			out.write("return result\n")
			
		elif "SelectAll" in procName:
			self.indent(out,2)
			out.write("result=cursor.fetchall()\n")
			self.indent(out,2)
			out.write("cursor.close()\n")
			self.indent(out,2)
			out.write("return result\n")
			
		else:
			self.indent(out,2)
			out.write("result=cursor.rowcount\n")
			self.indent(out,2)
			out.write("self.cnx.commit()\n")
			self.indent(out,2)
			out.write("cursor.close()\n")
			self.indent(out,2)
			out.write("return result\n")

		self.finishProcedure(out)

	def finishProcedure(self,out):
		out.write("\n")

"""
Generates PHP wrapper classes for stored procedures
Writes to the file ./PHP_CRUD_MySQL.php
"""
class MySQLPHPWrapperGenerator:

	def indent(self,out,n=1):
		for i in range(n):
			out.write("\t")
			
	def	processTable(self,out,tableName):
		out.write("\n// CRUD for table: "+tableName)
		out.write("\nclass "+tableName+"_CRUD{\n")
		self.indent(out)
		out.write("public $pdo;\n\n")
		self.indent(out)
		out.write("function dbConnect($host, $user, $pass, $dbname) {\n")
		self.indent(out,2)
		out.write("try {\n")
		self.indent(out,3)
		out.write("$dsn = sprintf(\"mysql:host=%s;dbname=%s;charset=utf8\", $host, $dbname);\n")
		self.indent(out,3)
		out.write("$option = array(\n")
		self.indent(out,4)
		out.write("PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC\n")
		self.indent(out,3)
		out.write(");\n")
		self.indent(out,3)
		out.write("$this->pdo=new PDO($dsn, $user, $pass, $option);\n")
		self.indent(out,2)
		out.write("} catch (PDOException $e) {\n")
		self.indent(out,3)
		out.write("exit('Error: ' . $e->getMessage());\n")
		self.indent(out,2)
		out.write("}\n")
		self.indent(out,1)
		out.write("}\n")

	def	finishTable(self,out):
		out.write("}\n")

	def processProcedure(self,out,procName,args):
		# Strip open/close parentheses
		args=args[1:-1]
		
		self.indent(out)
		# Function Signature
		out.write("public function "+procName+"CRUD(");

		if len(args):
			parms=[x.strip() for x in args.split(',')]
			parms=map(lambda x: x.split(' ') , parms)
			delim="$"
			for parm in parms:
				out.write(delim)
				out.write(parm[1])
				delim=",$"
				
		out.write("){\n")
		
		# Function Body
		self.indent(out,2)
		out.write("try{\n")
		self.indent(out,3)
		out.write("$sql=\"CALL "+procName+"(") 
		if len(args):
			argLen=len(args.split(","))
			delim="?"
			for i in range(argLen):
				out.write(delim)
				delim=",?"
				
		out.write(")\";\n")

		self.indent(out,3)
		out.write("$stmt=$this->pdo->prepare($sql);\n")
		
		if len(args) < 1:
			self.indent(out,3)
			out.write("$stmt->execute();\n")
			
		else:
			self.indent(out,3)
			out.write("$stmt->execute([")
			parms=[x.strip() for x in args.split(',')]
			parms=map(lambda x: x.split(' ') , parms)
			delim="$"
			for parm in parms:
				out.write(delim)
				out.write(parm[1])
				delim=",$"
				
			out.write("]);\n")


		if "SelectOne" in procName:
			self.indent(out,3)
			out.write("$rc=$stmt->fetch();\n")
			
		elif "SelectAll" in procName:
			self.indent(out,3)
			out.write("$rc=array();\n")
			self.indent(out,3)
			out.write("while($row=$stmt->fetch()){\n")
			self.indent(out,4)
			out.write("$rc[]=$row;\n")
			self.indent(out,3)
			out.write("}\n")
			
		else:
			self.indent(out,3)
			out.write("$rc=$stmt->rowCount();\n")
		
		self.finishProcedure(out)

	def finishProcedure(self,out):
		self.indent(out,3)
		out.write("$stmt=null;\n")
		self.indent(out,3)
		out.write("return $rc;\n")
		self.indent(out,2)
		out.write("} catch (PDOException $e) {\n")
		self.indent(out,3)
		out.write("exit('Error: ' . $e->getMessage());\n")
		self.indent(out,3)
		out.write("return FALSE;\n")
		self.indent(out,2)
		out.write("}\n")
		self.indent(out,2)
		out.write("return FALSE;\n")		
		self.indent(out)
		out.write("}\n")
			

class MySQLWrapper:
	lines=None
	
	def __init__(self,lines):
		self.lines=lines

	def wrap(self):
		php=MySQLPHPWrapperGenerator()
		py=MYSQLPythonWrapperGenerator()
		outPHP=open('./PHP_CRUD_MySQL.php','w')
		outPy=open('./PY_CRUD_MySQL.py','w')
		tableName=""
		for line in self.lines:
			if line.startswith("CREATE PROCEDURE "):
				b=len("CREATE PROCEDURE ")
				e=line.find("(")
				procName=line[b:e]
				args=line[e:]
				print("\t"+procName)
				#PHP
				php.processProcedure(outPHP,procName,args)
				#Python
				py.processProcedure(outPy,procName,args)
				
			elif line.startswith("-- TABLE: "):
				tableName=line[len("-- TABLE: "):]
				print("Processing "+tableName)
				#PHP
				php.processTable(outPHP,tableName)
				#Python
				py.processTable(outPy,tableName)

			elif line.startswith("-- END TABLE:"):
				#PHP
				php.finishTable(outPHP)
				#Python
				py.finishTable(outPy)
					
			elif line.startswith("-- DB: MySQL"):
				#PHP
				outPHP.write("<?php\n")
				print(line.replace("--","// CRUD for"),file=outPHP)
				#Python
				print(line.replace("--","# CRUD for"),file=outPy)
				outPy.write("import pymysql\n")
		
		outPHP.write("?>\n")
		outPHP.close()
		outPy.close()

"""
Entry point
"""
def wrap(args):
	lines=[line.strip() for line in open('./crudomatic_procedures.sql')]
	
	# TO DO: PostegresQL. Maybe MSSQL??
	if lines[0].startswith("-- DB: MySQL"): 
		w=MySQLWrapper(lines)
		w.wrap()
	else:
		print("Unsupported database: "+lines[0])

	return 0

if __name__ == '__main__':
	import sys
	sys.exit(wrap(sys.argv))
