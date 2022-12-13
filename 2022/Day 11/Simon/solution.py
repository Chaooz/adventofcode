#!/usr/local/bin/python3

import sys
from benedict import benedict

monkeys = []
yamlFile = "input.yaml"
superModulo = 1
class Monkey:
    def __init__(self, number, items, operation, test, targetMonkeyTrue, targetMonkeyFalse):
        self.number = number
        self.items = items
        self.operation = operation
        self.test = test
        self.ifTrue = targetMonkeyTrue
        self.ifFalse = targetMonkeyFalse
        self.itemsInspected = 0
    
    def throw(self, oldItem, newItem, targetMonkey):
        self.items.remove(oldItem)
        monkeys[targetMonkey].items.append(newItem)

def importMonkeysFromYaml(filename):
    monkeyImport = benedict.from_yaml(filename)
    global monkeys
    for monkey in monkeyImport:
        number = monkey[len(monkey)-1]
        items = str(monkeyImport[monkey]['Starting items']).split(',')
        items = [int(item) for item in items]
        operation = monkeyImport[monkey]['Operation'].split(' = ')[1]
        test = int(monkeyImport[monkey]['Test'].split(' ')[2])
        ifTrue = int(monkeyImport[monkey]['If true'].split(' ')[3])
        ifFalse = int(monkeyImport[monkey]['If false'].split(' ')[3])
            
        currentMonkey = Monkey(number, items, operation, test, ifTrue, ifFalse)
        monkeys.append(currentMonkey)

def calculateSuperModulo(monkeys):
    global superModulo
    monkeyTests = []
    for monkey in monkeys:
        monkeyTests.append(monkey.test)
    for number in monkeyTests:
        superModulo = superModulo * number
    
def monkeyTurn(monkey):
    tempItems = monkey.items.copy()
    for item in tempItems:
        # print("Beginning turn for monkey " + monkey.number + " with item " + str(item) + ".")
        monkey.itemsInspected += 1
        # print("Monkey " + monkey.number + " has inspected " + str(monkey.itemsInspected) + " items.")
        worriednessLevel = operation(monkey, item)
        # print("After inspecting " + str(item) + " your are " + str(worriednessLevel) + " worried.")
        worriednessLevel = int(worriednessLevel / 3)
        worried = worriednessTest(monkey, worriednessLevel)
        if worried:
            monkey.throw(item, worriednessLevel, monkey.ifTrue)
            # print("The monkey finds your concern amusing and throws the item at monkey " + str(monkey.ifTrue) + ".")
        else:
            monkey.throw(item, worriednessLevel, monkey.ifFalse)
            # print("The monkey is bored with the item and throws it at monkey " + str(monkey.ifFalse) + ".")

def monkeyTurn2(monkey):
    tempItems = monkey.items.copy()
    global superModulo
    for item in tempItems:
        # print("Beginning turn for monkey " + monkey.number + " with item " + str(item) + ".")
        monkey.itemsInspected += 1
        # print("Monkey " + monkey.number + " has inspected " + str(monkey.itemsInspected) + " items.")
        worriednessLevel = operation(monkey, item)
        # print("After inspecting " + str(item) + " your are " + str(worriednessLevel) + " worried.")
        worriednessLevel = int(worriednessLevel % superModulo)
        worried = worriednessTest(monkey, worriednessLevel)
        if worried:
            monkey.throw(item, worriednessLevel, monkey.ifTrue)
            # print("The monkey finds your concern amusing and throws the item at monkey " + str(monkey.ifTrue) + ".")
        else:
            monkey.throw(item, worriednessLevel, monkey.ifFalse)
            # print("The monkey is bored with the item and throws it at monkey " + str(monkey.ifFalse) + ".")

def worriednessTest(monkey, item):
    if item % monkey.test == 0:
        return True
    else:
        return False
    
def operation(monkey, item):
    old = item
    new = eval(monkey.operation)
    return new

def inspectedItems(monkey):
    return monkey.itemsInspected


importMonkeysFromYaml(yamlFile)

print("Solution part 1:")
iterations = 0

while iterations <= 19:
    for monkey in monkeys:
        monkeyTurn(monkey)
    iterations += 1

print("Iteration " + str(iterations) + " complete.")
for monkey in monkeys:
    print("Monkey: " + monkey.number + " is holding " + str(monkey.items) + " and has inspected " + str(monkey.itemsInspected) + " items.")

monkeys.sort(key=inspectedItems, reverse=True)
solution = monkeys[0].itemsInspected * monkeys[1].itemsInspected

print("The solution is " + str(solution))
print("----------------------------------------")

print("Solution part 2:")

iterations = 0
monkeys = []
importMonkeysFromYaml(yamlFile)
calculateSuperModulo(monkeys)
while iterations <= 9999:
    for monkey in monkeys:
        monkeyTurn2(monkey)
    iterations += 1
print("Iteration " + str(iterations) + " complete.")
for monkey in monkeys:
    print("Monkey: " + monkey.number + " is holding " + str(monkey.items) + " and has inspected " + str(monkey.itemsInspected) + " items.")

monkeys.sort(key=inspectedItems, reverse=True)
solution = monkeys[0].itemsInspected * monkeys[1].itemsInspected
print("The solution is " + str(solution))
