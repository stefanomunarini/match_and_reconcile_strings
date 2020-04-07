# Match and Reconcile
**Execution Instructions**

docker-compose up -d

Wait a few seconds then visit http://localhost:8080

**Aim**

The aim of this project is to enable actors to: import csv data into the system; retrieve information about musical works through their ISWC codes; export enriched data to CSV files.

The main problem of this project is the matching and reconciliation strategy.

A MusicalWork is an instance containing as metadata a title, an iswc, a list of contributors, and a source. When importing new data into the system, we want to add as much information as possible, preserving already existing data. It can happen, however, that some data coming from different sources, can have different formats (e.g. accents, special characters, addition of middle names, mispelled names, etc.).

To try solve and tackle this problem, when inserting new data regarding a Musical Work already existing in the system, the following strategy is applied:
1) if the new piece of data contains a valid iswc, the system tries to update the title, the list of contributors and the source
2) otherwise it uses the title as filter, and it updates the list of contributors:

In order to update the title, the system first normalize the string replacing accents and special characters with normal letters, and formats it capitalizing the first letter of each word.

In order to update the list of contributors, then, the system acts in the following way:
1) replace all accents and special characters with normal characters
2) capitalize first letter of each word
3) split the list of contributors
4) convert each of the contributor strings to a metaphone value
5) check whether the metaphone either equals one of the metaphone already saved in the instance, or if the two sequences matches with a threshold of at least 70%
6) If the point 5) is True, than the contributor is not added. Otherwise it is appened to the list of contributors