# td-query
Windows command line tool that issues a query on Treasure Data

# Quick Start Guide

The query.exe is a Windows command line tool that issues a query on Treasure Data 
and queries a database and a table to retrieve the records based on other optional
set of arguments.

The tool uses the Treasure Data's Python Client Library.  It requires the user to 
specify database name and table name along with optional arguments, for example
list of columns, timestamp, etc.  Please refer to the Help text for complete list 
of available arguments.

# Requirements

You need a Treasure Data account and a valid API key.

Please set the environment variable TD_API_KEY for the API key

For example,

	echo %TD_API_KEY%
  4321/9b4b781f9ab9e46c0b0555abef185dc123456789
  
# Installation

Two installation options

1. Download query.exe and run it on your Windows without any installation.

The query.exe is a single executable that bundled the codes and all of its dependencies.

However, this single executables is slower to start up (approximately 30-60 seconds
on our test server) than the second option because it uncompresses all dependencies
at the beginning of every run.

2. Download query.zip and unzip it on your Windows without any installation.

Run query.bat in the query folder.

# Examples

1. Run the tool without any arguments throws error, but short usage text is displayed

	query

		usage: query [-h] [-f {tabular,csv}] [-e {presto,hive}] [-c COL_LIST]
					 [-m MIN_TIME] [-M MAX_TIME] [-l LIMIT]
					 db_name table_name
		query: error: the following arguments are required: db_name, table_name

    Unsucessful run will exit with a non-0 return value

	echo %errorlevel%
		2

2. Run the tool with -h argument to display Help

	query -h

		usage: query [-h] [-f {tabular,csv}] [-e {presto,hive}] [-c COL_LIST]
					 [-m MIN_TIME] [-M MAX_TIME] [-l LIMIT]
					 db_name table_name

		Description: Query data from a table in a database on Treasure Data

		positional arguments:
		  db_name               Name of the database
		  table_name            Name of the table

		optional arguments:
		  -h, --help            show this help message and exit
		  -f {tabular,csv}, --format {tabular,csv}
								Output format: "tabular" or "csv" (default: tabular)
		  -e {presto,hive}, --engine {presto,hive}
								Query engine: "presto" or "hive" (default: presto)
		  -c COL_LIST, --col_list COL_LIST
								Comma separated list of columns; no space in between
								(default: all columns)
		  -m MIN_TIME, --min_time MIN_TIME
								Minimum UNIX timestamp in seconds (default: NULL)
		  -M MAX_TIME, --max_time MAX_TIME
								Maximum UNIX timestamp in seconds (default: NULL)
		  -l LIMIT, --limit LIMIT
								Limit of records returned (default: all records)

    Sucessful run will exit with a 0 return value

	echo %errorlevel%
		0

3. Run the tool with all arguments

	query -f csv -e hive -c 'first_name,last_name,city,time' -m 1468004460 -M 1483644180 -l 10 company_db employee_table

		first_name,last_name,city,time
		Yoko,Fishburne,New Haven,1482778860
		Lorrine,Worlds,Tampa,1482778860
		Junita,Stoltzman,Carson City,1482778860
		Lucy,Treston,Worcester,1482778860
		Lashaunda,Lizama,Hanover,1482778860
		Truman,Feichtner,Bloomfield,1482778860
		Mireya,Frerking,Pelham,1482778860
		Corinne,Loder,North Attleboro,1482778860
		Karan,Karpin,Beaverton,1481137260
		Hillary,Skulski,Homosassa,1481137260

4. MAX_TIME must be greater than MIN_TIME

	query -e hive -c 'first_name,last_name,city,time' -m 1483644180 -M 1468004460 -l 10 company_db employee_table
		ValueError: MAX_TIME must be greater than MIN_TIME

5. The tool selects the records whose timestamp is larger than MIN_TIME if only MIN_TIME is specified (no MAX_TIME)

	query -e hive -c 'first_name,last_name,phone1,time' -m 1483644180 -l 10 company_db employee_table

		+--------------+-------------+--------------+------------+
		| first_name   | last_name   | phone1       |       time |
		+==============+=============+==============+============+
		| Cheryl       | Haroldson   | 609-518-7697 | 1514834580 |
		+--------------+-------------+--------------+------------+
		| Arlene       | Klusman     | 504-710-5840 | 1514834580 |
		+--------------+-------------+--------------+------------+
		| Blair        | Malet       | 215-907-9111 | 1514834580 |
		+--------------+-------------+--------------+------------+
		| Jolanda      | Hanafan     | 207-458-9196 | 1514834580 |
		+--------------+-------------+--------------+------------+
		| Lauran       | Burnard     | 307-342-7795 | 1491420180 |
		+--------------+-------------+--------------+------------+
		| Filiberto    | Tawil       | 323-765-2528 | 1491420180 |
		+--------------+-------------+--------------+------------+
		| Ernest       | Syrop       | 301-998-9644 | 1491420180 |
		+--------------+-------------+--------------+------------+
		| Lashandra    | Klang       | 610-809-1818 | 1491420180 |
		+--------------+-------------+--------------+------------+
		| Benton       | Skursky     | 310-579-2907 | 1490788440 |
		+--------------+-------------+--------------+------------+
		| Alishia      | Sergi       | 212-860-1579 | 1490788440 |
		+--------------+-------------+--------------+------------+

6. The tool selects the records whose timestamp is smaller than MAX_TIME if only MAX_TIME is specified (no MIN_TIME)

	query -e hive -c 'time,county,last_name,phone2' -M 1483644180 -l 5 company_db employee_table

		+------------+------------+-------------+--------------+
		|       time | county     | last_name   | phone2       |
		+============+============+=============+==============+
		| 1466364180 | Cook       | Nievas      | 773-359-6109 |
		+------------+------------+-------------+--------------+
		| 1466362860 | Lackawanna | Drymon      | 570-868-8688 |
		+------------+------------+-------------+--------------+
		| 1466362860 | Macomb     | Lukasik     | 586-247-1614 |
		+------------+------------+-------------+--------------+
		| 1466362860 | New York   | Dhamer      | 212-225-9676 |
		+------------+------------+-------------+--------------+
		| 1466364180 | Essex      | Gehrett     | 973-986-4456 |
		+------------+------------+-------------+--------------+

7. The default query engine is Presto; If Presto is not enabled for your account, use -e hive argument for Hive query engine

	query -M 1483644180 -l 5 company_db employee_table
		Presto not enabled: Contact support or use query engine "hive"

8. The columns must be separated by comma without space in between

	query -e hive -c time,county,last_name -l 5 company_db employee_table

		+------------+----------------+-------------+
		|       time | county         | last_name   |
		+============+================+=============+
		| 1464722580 | Curry          | Chickering  |
		+------------+----------------+-------------+
		| 1464721260 | Richmond       | Mulqueen    |
		+------------+----------------+-------------+
		| 1464721260 | Baltimore City | Reitler     |
		+------------+----------------+-------------+
		| 1464722580 | Franklin       | Corrio      |
		+------------+----------------+-------------+
		| 1464721260 | Dona Ana       | Vocelka     |
		+------------+----------------+-------------+

9. The tool throws error if the list of the columns contains space in between

	query -e hive -c 'time,county, last_name' -l 5 company_db employee_table

		usage: query [-h] [-f {tabular,csv}] [-e {presto,hive}] [-c COL_LIST]
					 [-m MIN_TIME] [-M MAX_TIME] [-l LIMIT]
					 db_name table_name
		query: error: unrecognized arguments: employee_table

10. If the columns in the list do not exist in the table, the tool throws errors and lists the non-exist columns

	query -f csv -e hive -c 'firt_name,last_name,city1,time' -m 1468004460 -M 1483644180 -l 10 company_db employee_table
		Exception:  Column not found: firt_name,city1

11. List of the columns can be enclosed inside double-quotes or single-quotes; The example below shows the double-quotes

	query -e hive -c "time,county,last_name" -l 5 company_db employee_table

		+------------+----------------+-------------+
		|       time | county         | last_name   |
		+============+================+=============+
		| 1464722580 | Curry          | Chickering  |
		+------------+----------------+-------------+
		| 1464721260 | Richmond       | Mulqueen    |
		+------------+----------------+-------------+
		| 1464721260 | Baltimore City | Reitler     |
		+------------+----------------+-------------+
		| 1464722580 | Franklin       | Corrio      |
		+------------+----------------+-------------+
		| 1464721260 | Dona Ana       | Vocelka     |
		+------------+----------------+-------------+

12. Use only the arguments shown in Help text.  The example shows an unreconized -a argument

	query -e hive -a 5 company_db employee_table

		usage: query [-h] [-f {tabular,csv}] [-e {presto,hive}] [-c COL_LIST]
					 [-m MIN_TIME] [-M MAX_TIME] [-l LIMIT]
					 db_name table_name
		query: error: unrecognized arguments: -a employee_table

13. Without COL_LIST argument, the tool selects all columns

	query -e hive -l 5 company_db employee_table

		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+
		|   zip | city          | county         | phone2       | last_name   |    id | state   | first_name   | phone1       |       time |
		+=======+===============+================+==============+=============+=======+=========+==============+==============+============+
		| 88101 | Clovis        | Curry          | 505-950-1763 | Chickering  | 11191 | NM      | Devorah      | 505-975-8559 | 1464722580 |
		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+
		| 10309 | Staten Island | Richmond       | 718-654-7063 | Mulqueen    | 11192 | NY      | Timothy      | 718-332-6527 | 1464721260 |
		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+
		| 21215 | Baltimore     | Baltimore City | 410-957-6903 | Reitler     | 11187 | MD      | Laurel       | 410-520-4832 | 1464721260 |
		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+
		| 43215 | Columbus      | Franklin       | 614-648-3265 | Corrio      | 11141 | OH      | Ammie        | 614-801-9788 | 1464722580 |
		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+
		| 88011 | Las Cruces    | Dona Ana       | 505-335-5293 | Vocelka     | 11142 | NM      | Francine     | 505-977-3911 | 1464721260 |
		+-------+---------------+----------------+--------------+-------------+-------+---------+--------------+--------------+------------+

14. LIMIT argument must be greater than 0

	query -e hive -l -1 company_db employee_table

		ValueError: LIMIT must be greater than 0

15. Specify the format csv (-f csv) to return the ouput format in comma separated values

	query -e hive -f csv -m 1464721260 -M 1464921260 company_db employee_table

		zip,city,county,phone2,last_name,id,state,first_name,phone1,time
		88101,Clovis,Curry,505-950-1763,Chickering,11191,NM,Devorah,505-975-8559,1464722580
		10309,Staten Island,Richmond,718-654-7063,Mulqueen,11192,NY,Timothy,718-332-6527,1464721260
		21215,Baltimore,Baltimore City,410-957-6903,Reitler,11187,MD,Laurel,410-520-4832,1464721260
		43215,Columbus,Franklin,614-648-3265,Corrio,11141,OH,Ammie,614-801-9788,1464722580
		88011,Las Cruces,Dona Ana,505-335-5293,Vocelka,11142,NM,Francine,505-977-3911,1464721260
		66218,Shawnee,Johnson,913-899-1103,Caudy,11137,KS,Chanel,913-388-2079,1464721260
		96782,Pearl City,Honolulu,808-526-5863,Spickerman,11241,HI,Rolande,808-315-3077,1464722580
		80231,Denver,Denver,303-692-3118,Paulas,11242,CO,Howard,303-623-4241,1464721260
		7050,Orange,Essex,973-818-9788,Riopelle,11237,NJ,Talia,973-245-2133,1464721260
		94710,Berkeley,Alameda,510-942-5916,Degonia,11287,CA,Joesph,510-677-9785,1464721260
		94561,Oakley,Contra Costa,925-541-8521,Hiatt,11291,CA,Marguerita,925-634-7158,1464722580
		60623,Chicago,Cook,773-297-9391,Cookey,11292,IL,Carmela,773-494-4195,1464721260
		7866,Rockaway,Morris,973-225-6259,Madarang,11243,NJ,Kimbery,973-310-1634,1464747600
		32254,Jacksonville,Duval,904-514-9918,Honeywell,11193,FL,Arlette,904-775-4480,1464747600
		7660,Ridgefield Park,Bergen,201-387-9093,Stenseth,11143,NJ,Ernie,201-709-6245,1464747600
		7009,Cedar Grove,Essex,973-582-5469,Brideau,11293,NJ,Junita,973-943-3423,1464747600

16. Optional arguments can be placed after required arguments

	query company_db employee_table -e hive -f csv -m 1464721260 -M 1464921260

		zip,city,county,phone2,last_name,id,state,first_name,phone1,time
		7866,Rockaway,Morris,973-225-6259,Madarang,11243,NJ,Kimbery,973-310-1634,1464747600
		32254,Jacksonville,Duval,904-514-9918,Honeywell,11193,FL,Arlette,904-775-4480,1464747600
		7660,Ridgefield Park,Bergen,201-387-9093,Stenseth,11143,NJ,Ernie,201-709-6245,1464747600
		7009,Cedar Grove,Essex,973-582-5469,Brideau,11293,NJ,Junita,973-943-3423,1464747600
		88101,Clovis,Curry,505-950-1763,Chickering,11191,NM,Devorah,505-975-8559,1464722580
		10309,Staten Island,Richmond,718-654-7063,Mulqueen,11192,NY,Timothy,718-332-6527,1464721260
		21215,Baltimore,Baltimore City,410-957-6903,Reitler,11187,MD,Laurel,410-520-4832,1464721260
		43215,Columbus,Franklin,614-648-3265,Corrio,11141,OH,Ammie,614-801-9788,1464722580
		88011,Las Cruces,Dona Ana,505-335-5293,Vocelka,11142,NM,Francine,505-977-3911,1464721260
		66218,Shawnee,Johnson,913-899-1103,Caudy,11137,KS,Chanel,913-388-2079,1464721260
		96782,Pearl City,Honolulu,808-526-5863,Spickerman,11241,HI,Rolande,808-315-3077,1464722580
		80231,Denver,Denver,303-692-3118,Paulas,11242,CO,Howard,303-623-4241,1464721260
		7050,Orange,Essex,973-818-9788,Riopelle,11237,NJ,Talia,973-245-2133,1464721260
		94710,Berkeley,Alameda,510-942-5916,Degonia,11287,CA,Joesph,510-677-9785,1464721260
		94561,Oakley,Contra Costa,925-541-8521,Hiatt,11291,CA,Marguerita,925-634-7158,1464722580
		60623,Chicago,Cook,773-297-9391,Cookey,11292,IL,Carmela,773-494-4195,1464721260
