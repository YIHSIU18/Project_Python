import os
from flask import Flask,request,render_template
from datetime import date

#Defining Flask App
app = Flask(__name__)

#Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

#If this file doesn't exist, create it
if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt', 'w') as f:
        f.write('')
#Get a task list
def gettasklist():
    with open('tasks.txt', 'r') as f:
        tasklist=f.readlines()
    return tasklist

#Create new task list
def createnewtasklist():
    os.remove('tasks.txt')
    with open('tasks.txt', 'w') as f:
        f.write('')

#Update taks list
def updatetasklist(tasklist):
    os.remove('tasks.txt')
    with  open('tasks.txt', 'w') as f:
        f.writelines(tasklist)