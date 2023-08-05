import argparse
from termcolor import colored


class Cli:

    def __init__(self):
        self.author = "Overwatch Heir"
        self.version = "1.0"
        self.banner = r"""

                ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ██╗███████╗████████╗
                ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║     ██║██╔════╝╚══██╔══╝
                ███████╗██║   ██║██║     ██║███████║██║     ██║███████╗   ██║   
                ╚════██║██║   ██║██║     ██║██╔══██║██║     ██║╚════██║   ██║   
                ███████║╚██████╔╝╚██████╗██║██║  ██║███████╗██║███████║   ██║   
                ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝   ╚═╝ """ + '\n'

    def display_banner(self):
        print(colored(self.banner, 'red'))
        print(colored('             * Version: ' + self.version, 'red'))
        print(colored('             * Created by: ' + self.author, 'red'))
        print(colored("             * Take a look at README.md file for more info about the program\n", 'red'))

    def parse_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("-o", "--output", required=True, help="path to output wordlist ")
        parser.add_argument("-c", "--combinations", default=3, type=int, help="maximum number of words combinations "
                                                                              "-- default 2")
        return parser.parse_args()
