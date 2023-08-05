from validate_email import validate_email
from socialist.cli import Cli
from termcolor import colored
import datetime
import phonenumbers
import calendar


class Profile:

    def __init__(self):
        self.profile = {}
        self.now = datetime.datetime.now()
        self.cli = Cli()

    def identification(self):
        self.profile["first_name"] = str(
            input(colored("> First Name : ", 'yellow'))).replace(" ", "")
        self.profile["last_name"] = str(
            input(colored("> Last Name : ", 'yellow'))).replace(" ", "")
        self.profile["nickname"] = str(
            input(colored("> Nickname : ", 'yellow'))).replace(" ", "")
        self.profile["Id_number"] = str(
            input(colored("> ID-Number : ", 'yellow'))).replace(" ", "")

    def religion(self):
        religions = ['christianism', 'islam', 'judaism', 'budism', 'hinduism', 'none', 'other']
        religion_choice = str(
            input(colored("> Religion (christianism, islam, judaism, budism, hinduism, "
                                           "none, other): ", 'yellow'))).replace(" ", "")
        if religion_choice != "":
            while religion_choice not in religions:
                print(colored("\r\n[-] You must enter one of the options above!\n", 'red'))
                religion_choice = str(
                    input(colored("> Religion (christianism, muslim, judaism, budism, "
                                                   "hinduism, none, other): ", 'yellow'))).replace(" ", "")
            if religion_choice != 'none' or religion_choice != 'other':
                self.profile["religion"] = religion_choice

    def birth(self):
        birthdate = input(colored("> Birthdate (DDMMYYYY): ", 'yellow'))

        while len(birthdate) == 0 or len(birthdate) != 8:
            print(colored("\r\n[-] You must enter 8 digits for birthday!\n", 'red'))
            birthdate = input(colored("> Birthdate (DDMMYYYY): ", 'yellow'))

        self.profile["birth_day"] = str(birthdate[0:2])
        self.profile["birth_month"] = str(birthdate[2:4])
        self.profile["birth_year"] = str(birthdate[-4:])
        self.profile["age"] = str(self.now.year - int(birthdate[-4:]))

    def email(self):
        email_address = str(input(colored("> Email address : ", 'yellow'))).replace(" ", "")

        if email_address != "":
            while not validate_email(email_address, verify=True):
                print(colored("\r\n[-] Not valid! Email address does not exists!\n", 'red'))
                email_address = str(
                    input(colored("> Email address : ", 'yellow'))).replace(" ", "")

            self.profile["email_user"] = str(email_address.split('@')[0])

    def phone(self):
        phone = str(input(colored("> Phone Number : ", 'yellow')))
        if phone != "":
            phone_parsed = phonenumbers.parse(phone, None)

            while not phonenumbers.is_valid_number(phone_parsed):
                print(colored("\r\n[-] You must enter a correct phone number!\n",'red'))
                phone = str(input(colored("> Phone Number : ", 'yellow')))
                phone_parsed = phonenumbers.parse(phone, None)

            self.profile["phone_country"] = str(phone_parsed.country_code)
            self.profile["phone_number"] = str(phone_parsed.national_number)

    def education(self):
        self.profile["prim_school"] = str(
            input(colored("> Primary school : ", 'yellow'))).replace(" ", "")
        self.profile["sec_school"] = str(
            input(colored("> Secondary school : ", 'yellow'))).replace(" ", "")
        self.profile["university"] = str(
            input(colored("> University : ", 'yellow'))).replace(" ", "")

    def address(self):
        self.profile["street"] = str(
            input(colored("> Street address: ", 'yellow'))).replace(" ", "")
        self.profile["street_number"] = str(
            input(colored("> Street Number address: ", 'yellow'))).replace(" ", "")
        self.profile["floor"] = str(
            input(colored("> Floor adress : ", 'yellow'))).replace(" ", "")
        self.profile["door"] = str(
            input(colored("> Door adress : ", 'yellow'))).replace(" ", "")
        self.profile["post_code"] = str(
            input(colored("> Post Code : ", 'yellow'))).replace(" ", "")

    def politics(self):
        politics = ['liberal', 'conservative', "socialist ", "comunist", "anarchist", "christian-democrat",
                    "socialdemocrat", "other", "none"]
        orientation = str(input(colored("> Political orientation (liberal, conservative, "
                                                         "socialist,"
                                                         "comunist, anarchist, christian-democrat, socialdemocrat,"
                                                         "other, none ): "
                               , 'yellow'))).replace(" ", "")
        if orientation != "":
            while orientation not in politics:
                print(colored("\r\n[-] You must enter one of the above options!\n", 'red'))
                orientation = str(input(colored("> Political orientation (liberal, conservative, "
                                                                 "socialist,"
                                                                 "comunist, anarchist, christian-democrat, socialdemocrat,"
                                                                 "other, none ): "
                                       , 'yellow'))).replace(" ", "")
            if orientation != 'none' or orientation != 'other':
                self.profile["politics"] = orientation

    def car(self):
        self.profile["car_model"] = str(
            input(colored("> Car Model : ", 'yellow'))).replace(" ", "")
        self.profile["car_brand"] = str(
            input(colored("> Car Brand : ", 'yellow'))).replace(" ", "")
        self.profile["license_plate"] = str(
            input(colored("> License Plate : ", 'yellow'))).replace(" ", "")

    def motorcycle(self):
        self.profile["motorcycle_model"] = str(
            input(colored("> Motorcycle Model : ", 'yellow'))).replace(" ", "")
        self.profile["motorcycle_brand"] = str(
            input(colored("> Motorcycle Brand : ", 'yellow'))).replace(" ", "")
        self.profile["motorcycle_plate"] = str(
            input(colored("> Motorcycle License Plate : ", 'yellow'))).replace(" ", "")

    def work(self):
        self.profile["company"] = str(
            input(colored("> Company : ", 'yellow'))).replace(" ", "")
        self.profile["employee_id"] = str(
            input(colored("> Employee-ID : ", 'yellow'))).replace(" ", "")
        self.profile["position"] = str(
            input(colored("> Position : ", 'yellow'))).replace(" ", "")

    def hobbies(self):
        self.profile["colour"] = str(
            input(colored("> Colour : ", 'yellow'))).replace(" ", "")
        self.profile["pet"] = str(
            input(colored("> Pet Name : ", 'yellow'))).replace(" ", "")
        self.profile["music"] = str(
            input(colored("> Music Group : ", 'yellow'))).replace(" ", "")
        self.profile["artist"] = str(
            input(colored("> Music Artist : ", 'yellow'))).replace(" ", "")
        self.profile["film"] = str(input(colored("> Film  : ", 'yellow'))).replace(" ", "")
        self.profile["tv_show"] = str(
            input(colored("> TV Show  : ", 'yellow'))).replace(" ", "")
        self.profile["sport"] = str(input(colored("> Sport : ", 'yellow'))).replace(" ", "")
        self.profile["team"] = str(
            input(colored("> Sport Team: ", 'yellow'))).replace(" ", "")
        self.profile["city"] = str(input(colored("> City : ", 'yellow'))).replace(" ", "")
        self.profile["food"] = str(input(colored("> Food : ", 'yellow'))).replace(" ", "")
        self.profile["celebrity"] = str(
            input(colored("> Celebrity : ", 'yellow'))).replace(" ", "")

    def create(self, relative):
        print(colored("\n[+] Insert the information about the " + relative + " to make a dictionary\n"
                                                                                      "[+] If you don't know all the "
                                                                                      "info, just hit enter when asked!\n",
                               'green'))

        self.identification()
        self.religion()
        self.birth()
        self.email()
        self.phone()
        self.education()
        self.address()
        self.politics()
        self.car()
        self.motorcycle()
        self.work()
        self.hobbies()

    def batch(self):
        info = [self.profile["birth_day"],
                self.profile["birth_month"],
                calendar.month_name[int(self.profile["birth_month"])].lower(),
                calendar.month_name[int(self.profile["birth_month"])].capitalize(),
                calendar.month_name[int(self.profile["birth_month"])].upper(),
                calendar.month_abbr[int(self.profile["birth_month"])].lower(),
                calendar.month_abbr[int(self.profile["birth_month"])].capitalize(),
                calendar.month_abbr[int(self.profile["birth_month"])].upper(),
                self.profile["birth_year"],
                self.profile["birth_year"][-2:],
                self.profile["age"]]

        del self.profile["birth_day"]
        del self.profile["birth_month"]
        del self.profile["birth_year"]
        del self.profile["age"]

        for value in self.profile.values():
            if value != "":
                info.append(value.upper())
                info.append(value.lower())
                info.append(value.capitalize())

        return info
