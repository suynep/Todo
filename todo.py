#!/usr/bin/env python3

import os
import argparse
import datetime
from pprint import pprint
import csv
import sys

TODO_FILE = os.path.join(os.path.expanduser("~"), ".todo-py.csv")
HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".todo-py-history")

parser = argparse.ArgumentParser(
    prog="todo.py",
    description="A Simple Todo CLI Interface written in python\n\nAuthor: Suyash Nepal\nCreated On: Aug 2024",
    epilog="E-mail: suy.nepal@gmail.com\n\nThe only caveat while using this app:\nDO NOT USE `|` in your TASKS",
    formatter_class=argparse.RawTextHelpFormatter
)

# simply adding CLI args
parser.add_argument('-a', '--add', help="add a todo item to the list", type=str, metavar="ITEM")
parser.add_argument('-l', '--list', help="list the added todo items", action="store_true")
parser.add_argument('-d', '--done', help="mark the item in the INDEX as done || check -l for index ||", metavar="INDEX", type=int)
parser.add_argument('-p', '--progress', help="mark the item in INDEX as 'in-progress'", metavar="INDEX")
parser.add_argument('-r', '--remove', help="remove the local todo file", action="store_true")

# create a parser object to simplify future parsing actions
args = parser.parse_args()

if args.add != None:
    curr_index = 0
    if os.path.isfile(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            curr_index = len(f.readlines())

    with open(TODO_FILE, 'a+') as f:
        f.write(str(curr_index) + "|" +
                args.add + "|" +
                str(datetime.date.today()) +
                "\n"
        )

if args.list:
    if os.path.isfile(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            reader = csv.reader(f, delimiter="|")
            print('index', '\t', 'item', '\t', 'created-on')
            for row in reader:
                print(row[0], '\t', row[1], '\t', row[2])
    else:
        print("Please create a todo item first with\ntodo.py -a <item>")
        sys.exit(1)

if args.remove:
    if os.path.isfile(TODO_FILE):
        os.remove(TODO_FILE)
    else:
        print("Please create the todo file DB first with\ntodo.py -a <item>")
        sys.exit(1)

if args.done != None:
    index_to_remove = args.done
    lines = []
    with open(TODO_FILE, 'r') as f:
        dummy = f.readlines()
        lc = len(dummy)
        print(lc)
        if index_to_remove >= lc:
            print("Index out of bounds;\nPlease enter a valid INDEX")
            sys.exit(1)
        else:
            lines = dummy

    removed_line = lines.pop(index_to_remove)
    with open(TODO_FILE, 'w') as f:
        count = 0
        for line in lines:
            l = line[1:]
            line = str(count) + l
            f.write(line)
            count += 1

    with open(HISTORY_FILE, 'a+') as f:
        f.write("DONE: " + removed_line[2:])

    print("DONE: ", removed_line)
