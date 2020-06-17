import json
import os
import random
import requests

import pandas as pd
import networkx as nx

from copy import deepcopy
from datetime import datetime, timedelta
from faker import Faker

class Transaction:
    """
    Class that represents a transaction between two entities.

    When initializing a Transaction class, include the following parameters:
        origin:            (String) The source of the transaction.  This can be a credit card number, phone number, or email.
        destination:       (String) The target of the transaction.  This can be a company, phone number, or email.
        date:              (Datetime) A datetime object representing when the transaction occured. 
        amount:            (Int) A whole number representing how much of the transaction item was transferred. (Optional)
        transaction_type:  (String) The type of transaction that occured.  Valid types are "money", "email", or "phonecall"

    """
    def __init__(self, origin=None, destination=None, date=None, amount=None, transaction_type=None, x=None, y=None):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.x = x
        self.y = y

        self._validate_input_parameters()

    def __repr__(self):
        return repr((self.origin, self.destination, self.date, self.amount, self.transaction_type))

    def _validate_input_parameters(self):
        """ Validates the input parameters to determine they are of correct type and appropriate value.

        Raises:
            TypeError: Origin is not of type string.
            TypeError: Desination is not of type string.
            TypeError: Amount is not of type integer.
            TypeError: Transaction is not of type string.
            ValueError: Transaction Type was presented with an invalid string.
        """
        if type(self.origin) != str:
            print("Origin only accepts string inputs.")
            raise TypeError

        if type(self.destination) != str:
            print("Destination only accepts string inputs.")
            raise TypeError

        if type(self.amount) != int and self.amount is not None:
            print("Amount only accepts integer inputs.")
            raise TypeError

        if type(self.transaction_type) != str:
            print("Transaction types only accepts string inputs.")
            raise TypeError

        if self.transaction_type not in ['money', 'phonecall', 'email']:
            print("Transaction type only accepts 'money', 'email', or 'phonecall' as inputs.")
            raise ValueError
    
    def to_dict(self):
        """Method to export the class as a dictionary with a specific structure.

        Returns:
            [Dict] -- Dictionary representation of the class
        """
        return {"origin": self.origin,
                "destination": self.destination,
                "date": self.date,
                "amount": self.amount,
                "transaction-type": self.transaction_type,
                "x": self.x,
                "y": self.y}
        

class Person:
    """
    Class representation of a person.  Includes methods for adding additional details regarding person.

    When initializing a Person class the follow elements are needed:
        name:      (String) The name of the fake person.
        company:   (String) The fake company that employs the fake person.
        ssn:       (String) A fake social security number
        address:   (String) A valid address for the person.  This address will be geocoded.
        job:       (String) The job title for the person
        email:     (String) A person email account for the person.
        birthday:  (Date) The date of birth of the person.  This should be presented as a datetime object.
    """
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
        self.employee_number = None
        
        
        self.credit_card_transactions = []
        self.email_transactions = []
        self.phone_transactions = []
        self.coworker = []

    def __repr__(self):
        return repr((self._name, self._ssn, self._company))

    def to_dict(self):
        """Method to convert the class into a dictionary. Attaches any attributes assigned to the class.

        Returns:
            [Dict] -- Dictionary representation of the class.
        """
        person = {"name": self.name,
                  "company": self.company,
                  "ssn": self.ssn,
                  "address": self.address,
                  "job": self.job,
                  "email": self.email,
                  "birthday": self.birthday}

        
        try: person["work-email"] = self._work_email
        except: pass

        try: person["credit_card"] = self._credit_card
        except: pass

        try: person["phone_number"] = self._phone_number
        except: pass

        try: person["x"] = self._location_x
        except: pass

        try: person["y"] = self._location_y
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
    def coworker(self):
        return self._coworker
    @coworker.setter
    def coworker(self, value):
        self._coworker = value

    @property
    def employee_number(self):
        return self._employee_number
    @employee_number.setter
    def employee_number(self, value):
        self._employee_number = value

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
        """Method for adding credit card transactions to the class.
        This method takes the input and appends it to the credit_card_transactions list
        that is defined in the __init__ method.  

        Keyword Arguments:
            transaction {Transaction} -- Takes an input Transaction class object 
                                         and appends it to the credit_card_transactions 
                                         list. (default: {None})
        """
        self._credit_card_transactions.append(transaction)

    def add_email_transaction(self, transaction=None):
        """Method for adding email transactions to the class.
        This method takes the input and appends it to the email_transactions list
        that is defined in the __init__ method.  

        Keyword Arguments:
            transaction {Transaction} -- Takes an input Transaction class object 
                                         and appends it to the email_transactions 
                                         list. (default: {None})
        """
        self._email_transactions.append(transaction)

    def add_phone_transaction(self, transaction=None):
        """Method for adding phone transactions to the class.
        This method takes the input and appends it to the phone_transactions list
        that is defined in the __init__ method.  

        Keyword Arguments:
            transaction {Transaction} -- Takes an input Transaction class object 
                                         and appends it to the phone_transactions 
                                         list. (default: {None})
        """
        self._phone_transactions.append(transaction)

    def add_coworker(self, coworker=None):
        self._coworker.append(coworker)

    def get_coworkers(self):
        coworkers = []
        worker = self.to_dict()
        for c in self._coworker:
            coworker = deepcopy(worker)
            coworker['coworker'] = c
            coworkers.append(coworker)

        return coworkers

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

        self.G = None

        self.start_date = datetime.today() - timedelta(days=30)

        self.people = []
        self.companies = []
        self.email_addresses = []
        self.phone_numbers = []

        self.company_addresses = {}

        self.execute()

    def _get_companies_list(self):
        self.companies = [person.company for person in self.people]

    def _get_email_list(self):
        self.email_addresses = [person.work_email for person in self.people]

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
    
    def _create_random_graph(self, graph_type=None, number_of_people=0):
        if graph_type not in ['Tree', 'Random']:
            print("Please enter a valid random graph type.")
            raise ValueError

        if number_of_people == 0:
            print("Please enter a number greater than zero for the number of people")
            raise ValueError

        if graph_type == 'Tree' and number_of_people > 0:
            self.G = nx.random_tree(number_of_people)
            return True
        
        if graph_type == 'Random':
            return False
    
    def _create_fake_people(self, number_of_people=0):

        if number_of_people > 0 and self.G is None:
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

        if number_of_people > 0 and self.G is not None:
            count = 0

            company = ""

            for node in self.G.nodes(data=True):
                profile = self.fake.profile()

                if count == 0:
                    company = profile['company']
                else:
                    profile['company'] = company

                self.G.nodes[count]['name'] = profile['name']

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

                person.employee_number = count

                self.people.append(person)
                count +=1

                print(person)

            for person in self.people:
                neighbor_list = list(nx.neighbors(self.G, person.employee_number))
                for neighbor in neighbor_list:
                    person.add_coworker(self.G.nodes[neighbor]['name'])

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

        elif transaction_type is "coworker":
            for person in self.people:
                for coworker in person.get_coworkers():
                    data.append(coworker)
        
        elif transaction_type is "people":
            for person in self.people:
                data.append(person.to_dict())

        df = pd.DataFrame(data)
        df.to_csv(transaction_type + ".csv")           
    
    def execute(self):

        num_people = int(input("How many people would you like to create? (Please enter whole number):  "))
        graph_type = str(input("What type of graph would you like to create? (Tree or Random): "))
        print(graph_type, num_people)
        
        tree = self._create_random_graph(graph_type, num_people)

        self._create_fake_people(num_people)
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
        if tree:
            self._to_pandas_dataframe("coworker")

DataFaker()