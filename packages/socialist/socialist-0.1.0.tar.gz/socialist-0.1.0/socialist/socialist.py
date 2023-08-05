from itertools import permutations
from tqdm import tqdm
from socialist.cli import *
from socialist.profile import Profile
import string


info = []


def add_profile(name):
    profile = Profile()
    profile.create(name)
    profile_info = profile.batch()
    info.extend(profile_info)

    del profile


def socialist(args):
    output_file = open(args.output, 'w+')
    print(colored("\r\n[+] Now making a password list with the info you provided...", 'green'))

    for n in range(1, args.combinations + 1):
        print(colored("\n" + str(n) + " words combinations", 'green'))
        num_lines = sum(1 for _ in permutations(info, n))

        for group in tqdm(permutations(info, n), total=num_lines, ncols=100):
            if n == 1:
                output_file.write(''.join(group) + "\n")
            else:
                for element in string.punctuation:
                    output_file.write(element.join(group) + "\n")
                    output_file.write(element.join(group) + "\n")

    print(colored("\r\n[+] Password list successfully created!\n", 'green'))


def main():

    cli = Cli()
    cli.display_banner()

    add_profile('victim')

    more_questions = str(input(colored("\r\n[+] If you want, we will make YES or NO questions related to the "
                                              "victim's relatives to improve the password list... "
                                              "Do you agree ? (yes/no) : ", 'green')))

    if more_questions == 'yes':

        has_partner = str(input(colored("\r\n[+] Does the victim have a partner ? (yes/no) : ", 'green')))

        if has_partner == 'yes':
            add_profile('partner')

        has_expartners = str(
            input(colored("\r\n[+] Does the victim have a expartners ? (yes/no) : ", 'green')))

        if has_expartners == 'yes':
            expartners_number = int(input(colored("  [+] How many expartners has the victim ? : ", 'green')))
            while expartners_number == 0:
                print(colored(("  [-] You must enter an integer for the number of expartners!", 'red')))
                expartners_number = int(
                    input(colored("  [+] How many expartners has the victim ?  : ", 'green')))

            for n in range(0, expartners_number):
                add_profile('expartner ' + str(n + 1))

        has_father = str(input(colored("\r\n[+] Does the victim have a father ? (yes/no) : ", 'green')))

        if has_father == 'yes':
            add_profile('father')

        has_mother = str(input(colored("\r\n[+] Does the victim have a mother ? (yes/no) : ", 'green')))

        if has_mother == 'yes':
            add_profile('mother')

        has_children = str(input(colored("\r\n[+] Does the victim have children ? (yes/no) : ", 'green')))

        if has_children == 'yes':
            children_number = int(input(colored("  [+] How many children has the victim ? : ", 'green')))

            while children_number == 0:
                print(colored(("  [-] You must enter an integer for the number of children!", 'red')))
                children_number = int(input(colored("  [+] How many children has the victim ?  : ", 'green')))

            for n in range(0, children_number):
                add_profile('child ' + str(n + 1))

    socialist(cli.parse_args())


if __name__ == '__main__':
    main()
