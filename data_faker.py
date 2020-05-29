import json
import os
import random
import requests

import pandas as pd

from datetime import datetime, timedelta
from faker import Faker

class Transaction:
    def __init__(self, origin=None, destination=None, date=None, amount=None, transaction_type=None, x=None, y=None):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.x = x
        self.y = y

    def __repr__(self):
        return repr((self.origin, self.destination, self.date, self.amount, self.transaction_type))

    def to_dict(self):
        return {"origin": self.origin,
                "destination": self.destination,
                "date": self.date,
                "amount": self.amount,
                "transaction-type": self.transaction_type,
                "x": self.x,
                "y": self.y}
        

class Person:
    def __init__(self, name, company, ssn, address, job, email, birthday):
        self.name = name
        self.company = company
        self.ssn = ssn
        self.address = address
        self.job = job
        self.email = email
        self.birthday = birthday

        self.work_email = None
        self.credit_card = None
        self.phone_number = None
        self.location_x = None
        self.location_y = None
        
        self.credit_card_transactions = []
        self.email_transactions = []
        self.phone_transactions = []

    def __repr__(self):
        return repr((self._name, self._ssn, self._company))

    def to_dict(self):
        person = {"name": self.name,
                  "company": self.company,
                  "ssn": self.ssn,
                  "address": self.address,
                  "job": self.job,
                  "email": self.email,
                  "birthday": self.birthday}

        
        try: person["work-email"] = self.work_email
        except: pass

        try: person["credit_card"] = self.credit_card
        except: pass

        try: person["phone_number"] = self.phone_number
        except: pass

        try: person["x"] = self.location_x
        except: pass

        try: person["y"] = self.location_y
        except: pass

        return person

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def company(self):
        return self._company
    @company.setter
    def company(self, value):
        self._company = value

    @property
    def ssn(self):
        return self._ssn
    @ssn.setter
    def ssn(self, value):
        self._ssn = value

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = value

    @property
    def job(self):
        return self._job
    @job.setter
    def job(self, value):
        self._job = value

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value

    @property
    def birthday(self):
        return self._birthday
    @birthday.setter
    def birthday(self, value):
        self._birthday = value

    @property
    def work_email(self):
        return self._work_email
    @work_email.setter
    def work_email(self, value):
        self._work_email = value

    @property
    def credit_card(self):
        return self._credit_card
    @credit_card.setter
    def credit_card(self, value):
        self._credit_card = value

    @property
    def phone_number(self):
        return self._phone_number
    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value

    @property
    def credit_card_transactions(self):
        return self._credit_card_transactions
    @credit_card_transactions.setter
    def credit_card_transactions(self, value):
        self._credit_card_transactions = value

    @property
    def email_transactions(self):
        return self._email_transactions
    @email_transactions.setter
    def email_transactions(self, value):
        self._email_transactions = value

    @property
    def phone_transactions(self):
        return self._phone_transactions
    @phone_transactions.setter
    def phone_transactions(self, value):
        self._phone_transactions = value

    @property
    def location_x(self):
        return self._location_x
    @location_x.setter
    def location_x(self, value):
        self._location_x = value

    @property
    def location_y(self):
        return self._location_y
    @location_y.setter
    def location_y(self, value):
        self._location_y = value

    def add_credit_card_transaction(self, transaction=None):
        self._credit_card_transactions.append(transaction)

    def add_email_transaction(self, transaction=None):
        self._email_transactions.append(transaction)

    def add_phone_transaction(self, transaction=None):
        self._phone_transactions.append(transaction)

    def get_credit_card_transactions(self):
        transactions = []

        for t in self._credit_card_transactions:
            transactions.append(t.to_dict())

        return transactions

    def get_email_transactions(self):
        transactions = []

        for t in self._email_transactions:
            transactions.append(t.to_dict())

        return transactions

    def get_phone_transactions(self):
        transactions = []

        for t in self._phone_transactions:
            transactions.append(t.to_dict())

        return transactions
    

class DataFaker:
    def __init__(self):
        
        self.fake = Faker()
        Faker.seed(0)

        self.start_date = datetime.today() - timedelta(days=30)

        self.people = []
        self.companies = []
        self.email_addresses = []
        self.phone_numbers = []

        self.company_addresses = {}

        self.execute()

    def _get_companies_list(self):
        for person in self.people:
            self.companies.append(person.company)

    def _get_email_list(self):
        for person in self.people:
            self.email_addresses.append(person.work_email)

    def geocode_address(self, address=None):
        """Use World Geocoder to get XY for one address at a time."""
        querystring = {
            "f": "json",
            "singleLine": address}
        url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"  # noqa: E501
        response = requests.request("GET", url, params=querystring)
        p = response.text
        j = json.loads(p)
        location = j['candidates'][0]['location']  # returns first location as X, Y
        return location
    
    def _create_fake_people(self):

        num_people = int(input("How many people would you like to create? (Please enter whole number):  "))

        if num_people > 0:
            for _ in range(num_people):
                profile = self.fake.profile()
                person = Person(name=profile['name'],
                                company=profile['company'],
                                ssn=profile['ssn'],
                                address=profile['residence'],
                                job=profile['job'],
                                email=profile['mail'],
                                birthday=profile['birthdate'])

                location = self.geocode_address(profile['residence'])

                self.company_addresses[profile['company']] = location
                
                person.location_x = location['x']
                person.location_y = location['y']

                self.people.append(person)
                print(person)

        return

    def _create_fake_work_email(self):
        work_email = str(input("Would you like a work email addresses created? (y/n):  "))

        if work_email not in ['y', 'n']:
            print("Invalid selection.  Please enter y or n.")
            work_email = str(input("Would you like a work email addresses created?:  "))
        
        if work_email is 'y':
            for person in self.people:
                person.work_email = person.name.replace(" ", ".") + "@" + self.fake.domain_name()    
            return True

        else:
            return False

    def _create_fake_phone_number(self):
        phone_number = str(input("Would you like a phone number created? (y/n):  "))

        if phone_number not in ['y', 'n']:
            print("Invalid selection.  Please enter y or n.")
            phone_number = str(input("Would you like a phone number created? (y/n):  "))
        
        if phone_number is 'y':
            for person in self.people:
                person.phone_number = self.fake.phone_number()
                self.phone_numbers.append(person.phone_number)
            return True

        else:
            return False

    def _create_fake_credit_card(self):
        credit_card = str(input("Would you like a fake credit card created? (y/n):  "))

        if credit_card not in ['y', 'n']:
            print("Invalid selection.  Please enter y or n.")
            credit_card= str(input("Would you like a fake credit card created? (y/n):  "))

        if credit_card is 'y':
            for person in self.people:
                person.credit_card = self.fake.credit_card_number()
            return True
        
        else:
            return False

    def _generate_transactions(self, transaction_type=None):
        transactions = str(input(f"Would you like to generate fake {transaction_type} transactions? (y/n):  "))

        if transactions not in ['y', 'n']:
            print("Invalid selection.  Please enter y or n.")
            transactions = str(input(f"Would you like to generate fake {transaction_type} transactions? (y/n):  "))
        

        for person in self.people:
            for _ in range(random.randint(1, 10)):

                if transaction_type is "money":
                    receiving_party = random.choice(self.companies)
                    transaction = Transaction(origin=person.credit_card,
                                            destination=receiving_party,
                                            date=self.fake.date_time_between(self.start_date, end_date='now'),
                                            amount=random.randint(1, 1000),
                                            transaction_type=transaction_type,
                                            x=self.company_addresses[receiving_party]['x'],
                                            y=self.company_addresses[receiving_party]['y'])


                    person.add_credit_card_transaction(transaction)

                elif transaction_type is "email":
                    transaction = Transaction(origin=person.work_email,
                                              destination=random.choice(self.email_addresses),
                                              date=self.fake.date_time_between(self.start_date, end_date='now'),
                                              amount=None,
                                              transaction_type=transaction_type,
                                              x=person.location_x,
                                              y=person.location_y)

                    if transaction.origin != transaction.destination:
                        person.add_email_transaction(transaction)

                elif transaction_type is "phonecall":
                    transaction = Transaction(origin=person.phone_number,
                                              destination=random.choice(self.phone_numbers),
                                              date=self.fake.date_time_between(self.start_date, end_date='now'),
                                              amount=None,
                                              transaction_type=transaction_type,
                                              x=person.location_x,
                                              y=person.location_y)

                    if transaction.origin != transaction.destination:
                        person.add_phone_transaction(transaction)

    def _to_pandas_dataframe(self, transaction_type=None):
        data = []
        
        if transaction_type is "money":
            for person in self.people:
                for purchase in person.get_credit_card_transactions():
                    data.append(purchase)

        elif transaction_type is "email":
            for person in self.people:
                for email in person.get_email_transactions():
                    data.append(email)

        elif transaction_type is "phonecall":
            for person in self.people:
                for call in person.get_phone_transactions():
                    data.append(call)

        elif transaction_type is "people":
            for person in self.people:
                data.append(person.to_dict())

        df = pd.DataFrame(data)
        df.to_csv(transaction_type + ".csv")           
    
    def execute(self):

        self._create_fake_people()
        self._get_companies_list()

        phone_number = self._create_fake_phone_number()
        if phone_number:
            self._generate_transactions("phonecall")
            self._to_pandas_dataframe("phonecall")

        email = self._create_fake_work_email()
        if email:
            self._get_email_list()
            self._generate_transactions("email")
            self._to_pandas_dataframe("email")
        
        credit_card = self._create_fake_credit_card()
        if credit_card:
            self._generate_transactions("money")
            self._to_pandas_dataframe("money")

        self._to_pandas_dataframe("people")

DataFaker()