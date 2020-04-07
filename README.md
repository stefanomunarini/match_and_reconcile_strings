# Match and Reconcile
**Execution Instructions**

docker-compose up -d

Wait a few seconds then visit http://localhost:8080

**Aim**

The aim of this project is to enable actors to: import csv data into the system; retrieve information about musical works through their ISWC codes; export enriched data to CSV files.

**Problem**

The main problem of this project is the matching and reconciliation strategy.

A MusicalWork is an instance containing as metadata a title, an iswc, a list of contributors, and a source. When importing new data into the system, we want to add as much information as possible, preserving already existing data. It can happen, however, that some data coming from different sources, has different formats (e.g. accents, special characters, addition of middle names, mispelled names, etc.).

To try solve and tackle this problem, when inserting new data regarding a Musical Work already existing in the system, the following strategy is applied:
1) if the new piece of data contains a valid iswc, the system tries to update the title, the list of contributors and the source
2) otherwise it uses the title as filter, and it updates the list of contributors:

**Update strategy**

***Title***

When inserting a new record, the system normalizes the title first, replacing accents and special characters with normal letters, and capitalizing the first letter of each word.

***Contributors***

In order to add or update the list of contributors, then, the system acts in the following way:
1) replace all accents and special characters with normal characters
2) capitalize first letter of each word
3) split the list of contributors passed as input and the list of contributors already saved in the instance
4) convert each of the contributor strings (of both lists) to a metaphone value
5) loop through all the new contributor list, checking whether the metaphone of a contributor equals one of the contributor metaphone already saved in the instance, or if the two sequences matches with a threshold of at least 70% (this last one is for cases where a middle name is added: e.g. Andrea Luca and Andrea Mario Luca)
6) If the point 5) validates, than the contributor is not added (as the contributor being added is already present in the instance). Otherwise it is appened to the list of contributors.
