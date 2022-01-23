#Url-Scan - README:

Description:

Url-Scan is a program for searching url scans performed by the online service urlscan.io (https://urlscan.io). The program gets a list of queries and returns for each query the the urls and screenshot of the pages detected as malicious by urlscan.io service.

Running:

Run the program, in the program console input line, enter a single query or a list of queries separated by a comma. The queries must be ElasticSearch query string queries.

Algorithm Description:

The program get the queries as an input.

Quotas management:

The program gets current quotas of the user by using Http GET request to urlscan.io Quotas API.
If the user exceeded the hourly/daily quota, the program will stop sending queries for searching, and will return the results it has till that point.
If the minutely quota of the user was exceeded, the program waits for one minute, waiting for the urlscan.io service to reset the minutely quota,

Current minimal quota is calculated - minimum of day, hour and minute quota.
For each query of the queries list, up to the number of quota, a scan search and result processing is executed in a different thread.
If the number of queries is bigger than the minute quota, the program waits for a minute. After a minute, the program gets the current quotas again and continues the process.

* I chose waiting for the minute quota to reset in the program because I assumed that for a program that supposed to run a few times a day (twice a day), for big amount of queries, it is acceptable for the running time to be longer and wait for the minute quota to reset, for the benefit of searching as many queries as possible from the users input in a certain run.
* Larger quotas will increase efficiency and running the program with query list smaller than the minute quota will not suffer from this decrease in efficiency.


Searching Url Scans by Query:

Each thread runs search_scans_by_query function, the function sends a Http GET request to the urlscan.io Search API.
If the total number of results for a query in the response is bigger than 100, the API returns only the first 100 results, for getting the following results the programs sends the same Http GET, with a “search_after” property in the payload, contains an identifier of the last result received.
The response received for the Http GET request contains a lot of data, the program coverts the data so that the program returned from the program contains the url and a path to a screenshot of paged marked as malicious by urlscan.io service in previous scans.

*The program has config_file contains the urls for urscan.io APIs and the user api-key for accessing the API.

Multithreading:

* I chose to implement the program using multithreading access, I found it efficient for the amount of searches requested in the task (hundreds of queries).

* Although Python interpreter use of GIL, I found the use of multithreading in this task efficient since the program performance is i/o bounded, so the asynchrony between the threads can be useful during i/o waiting time.

* For bigger scales (thousands and more) I might need to use another approach and architecture.

