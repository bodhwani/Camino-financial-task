import json
from dateutil.parser import parse
import datetime
from collections import OrderedDict
from json import JSONDecoder

f = open("data.json", "r")
data = f.read()
#remove "[" at the beginning and "]" from the end.
data = data[1:-1]
decode_data = JSONDecoder(object_pairs_hook=OrderedDict)
decode_data = decode_data.decode(data)
pk = decode_data["pk"]
fields = decode_data["fields"]
dic_keys = fields.keys()

table_name = "myTable"

# CREATE query: 

def checktype(datatype):

	if datatype is None:
		return "VARCHAR(100)"
	elif isinstance(datatype, bool):
		return "BIT NOT NULL"
	elif isinstance(datatype,int):
		return "INT NOT NULL"
	
	elif "xml" in datatype:
		return "XML NOT NULL"
	elif isinstance(datatype, str):
		try:
			#try to parse the datatype into date format
			v_date = parse(datatype)
		except:
			return "VARCHAR(" + str(len(datatype)) + ") NOT NULL"
		else:
			return "DATE NOT NULL"
 

sql = "CREATE TABLE " + table_name + "("  + "\n" 

#primary key counter
pk_counter = 1

for entry,datatype in fields.items():
	if pk_counter == pk:
		sql += str(entry) + "\t" + checktype(datatype) + " PRIMARY KEY" + "," + "\n"
	else:
		sql += str(entry) + "\t" + checktype(datatype) + "," + "\n"
	pk_counter+=1
sql = sql[:-2]
sql += ")"

fs = open("output.sql", "w")
fs.write(sql)
fs.write("\n\n")


#INSERT query:

insert_sql = "INSERT INTO " + table_name + "("
insert_datatype = " VALUES ("
for entry,datatype in fields.items():
	insert_sql += str(entry) + ","
	if datatype is None:
		insert_datatype += str("NULL") + ","
	elif isinstance(datatype, int):
		insert_datatype += str(datatype) + ","
	else:
		insert_datatype += "'" + str(datatype) + "'" + ","

insert_datatype = insert_datatype[:-1]
insert_sql = insert_sql[:-1]
insert_sql += ")"
insert_datatype += ")" 
insert_query = insert_sql + insert_datatype

fs.write(insert_query)