# Cherry-Picking Algorithm - README:

## Description:

Cherry-Picking Algorithm is an algorithm for selecting the 4-most important alerts from an input list of alerts. Importance is determined by the alert’s properties: type, subtype, title identifiers and date, according to a priority map.

## Running:

For running the algorithm replace the list of alerts in the variable “alerts” in “alerts_input.py” file and run the program.

## Algorithm Description:

### Building type-subtype-map

When AlertPicker object is created, a type-subtype map is created.
Type-subtype map is a dictionary, maps keys: string represents type + subtype concatenation, to values: a list contains: in index 0: int represents the priority in range 1-6, in index 1: list of strings that are the title-identifiers for alerts of this type and subtype.
The data used for creating this map is from the file “alert_priority_map.py” (Appendix A.1 in the task description).

### Sort, Title-Identifiers Search and Picking

#### Sort:

Alert input list is sorted by Type+SubType priority (according to the type-subtype-map) in ascending order, then by FoundDate in descending order.

#### Title-Identifiers Searching:

The algorithm goes throw the sorted alerts, and checks if the alert’s title contains at least one of the title-identifiers belongs to the alert’s type+subtype (according to the type-subtype-map).
If it does, the alert id is added to a list.
this phase is executed until 4 alerts are picked (the list contains 4 alert_ids).

## Time Complexity:

* Building type-subtype-map - O(1) since there is a constant number of priorities.
* Sort: O(nlogn)
* Title-Identifiers Searching:
  * Searching for a substring in a title string is done in O(title-length).
  * On the worst-case scenario this phase will be executed for all n alerts in the list, but on the average case there will be fewer executions, only until 4 alerts are picked, because of the list sorting.
  * O(n * a * b) => O(n)
  * a = average number of title_identifiers strings
  * b = average length of title_identifier string
  * I assumed a and b are constants.

* Conclusion: **O(nlogn)**


## Other Implementation Option:

* Bucket sorting the alerts by type+subtype priority.
* Sort the first priority bucket alerts by date.
* Title-Identifiers search for the first priority alerts.
* Only if there are less than 4 alerts picked we continue sorting the next priority bucket by date.

* In the worst-case scenario this implementation complexity will be also O(nlogn), but in the average case it will be more efficient: ~O(n).

* I chose the first implementation because I thought it is efficient enough for the problem presented in the task. In addition, It is a more simple solution for the problem.
