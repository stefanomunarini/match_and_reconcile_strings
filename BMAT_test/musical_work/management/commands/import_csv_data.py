import csv
from difflib import SequenceMatcher

import requests
import unidecode
from django.core.management import BaseCommand
from metaphone import doublemetaphone

from musical_work.models import MusicalWork


class Command(BaseCommand):
    help = "Import data from a CSV file."

    elements_to_be_checked_as_last = []
    errors_while_inserting = []

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **kwargs):

        url = kwargs.get("url")[0]

        with requests.Session() as s:
            csv_file = s.get(url)
            decoded_content = csv_file.content.decode('utf-8')
            reader = csv.reader(decoded_content.splitlines(), delimiter=',')
            data = list(reader)

            for record in data[1:]:
                self._create_or_update_musicalwork(record)

            for row in self.elements_to_be_checked_as_last:
                self._create_or_update_musicalwork(row, last_check=True)

            if self.errors_while_inserting:
                print("\033[91mFailed to insert some elements:\033[0m")
                for error in self.errors_while_inserting:
                    print("\033[93m{}\033[0m".format(str(error)))

    def _create_or_update_musicalwork(self, row, last_check=False):
        title = row[0]
        contributors = row[1]
        iswc = row[2]

        created = False
        if iswc:
            instance, created = MusicalWork.objects.get_or_create(iswc=iswc)
        else:
            instance = MusicalWork.objects.filter(title=title)
            if not instance.exists():
                if last_check:
                    row.append("ERROR details: IWSC not provided and record with title '{}' not found".format(title))
                    self.errors_while_inserting.append(row)
                    return
                self.elements_to_be_checked_as_last.append(row)
                return

        if not isinstance(instance, MusicalWork):
            instance = instance.first()
        if created:
            self._add_title(instance, title)

        self.__add_or_updated_contributors(instance, contributors)

    def __normalize_word(self, word, title_style=False):
        # capitalize first letter of each word
        if title_style:
            word = word.title()

        # Remove accents
        return unidecode.unidecode(word)

    def __add_or_updated_contributors(self, instance, contributors):

        contributors = self.__normalize_word(contributors, title_style=True)

        if instance.contributors:

            instance_contributors_list = instance.contributors.split("|")
            row_contributor_list = contributors.split("|")

            intance_contributors_metaphones = [doublemetaphone(contrib) for contrib in instance_contributors_list]

            for row_contributor in row_contributor_list:

                row_contributor_metaphone = doublemetaphone(row_contributor)
                if not self._metaphones_match(row_contributor_metaphone, intance_contributors_metaphones):
                    instance.contributors = instance.contributors + "|" + row_contributor

        else:
            instance.contributors = contributors

        instance.save()

    def _add_title(self, instance, title):

        # reinforce the check for instance creation (an already existing instance has always a title)
        if not instance.title:
            normalized_title = self.__normalize_word(title)
            instance.title = normalized_title

            instance.save()

    def _metaphones_match(self, contributor_metaphone, instance_contributors_metaphones):

        # if "" in contributor_metaphone:

        for instance_contributor_metaphone in instance_contributors_metaphones:

            if (contributor_metaphone[1] == instance_contributor_metaphone[1] or \
                SequenceMatcher(None, contributor_metaphone[1], instance_contributor_metaphone[1]).ratio() >= 0.7) and \
                    contributor_metaphone[1] != "":
                return True

            if (contributor_metaphone[0] == instance_contributor_metaphone[1] or
                SequenceMatcher(None, contributor_metaphone[0], instance_contributor_metaphone[1]).ratio() >= 0.7) and \
                    contributor_metaphone[0] != "" or \
                (contributor_metaphone[1] == instance_contributor_metaphone[0] or \
                SequenceMatcher(None, contributor_metaphone[1], instance_contributor_metaphone[0]).ratio() >= 0.7) and \
                    contributor_metaphone[1] != "":
                return True
            else:
                if (contributor_metaphone[0] == instance_contributor_metaphone[0] or \
                    SequenceMatcher(None, contributor_metaphone[0],
                                    instance_contributor_metaphone[0]).ratio() >= 0.7) and \
                        contributor_metaphone[0] != "":
                    return True
        return False
