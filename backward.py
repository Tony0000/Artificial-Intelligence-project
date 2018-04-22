import re

RULE_SEPARATOR = ";"
ENT_SEPARATOR = "=>"
AND = "&"
OR = "#"

class Backwards(object):

    def __init__(self, raw_facts, raw_rules):
        self.facts = raw_facts
        self.rules = raw_rules
        self.entailments = {}
        self.queue = list()
        self.solution = ''

        self.setUp()

    def setUp(self):
        # Seting up facts
        self.facts = set(self.facts.split(","))
        self.facts.add(True)

        # Verifying rules
        self.cleanRules(self.rules)

    def cleanRules(self, raw_rules):
        # Cleaning rules
        raw_rules = raw_rules.lower()
        raw_rules = re.sub(r'\s+','', raw_rules)
        self.rules = raw_rules.split(sep=RULE_SEPARATOR)
        for rule in self.rules:
            if(self.isValid(rule)):
                statements = rule.split(sep=ENT_SEPARATOR)
                self.entailments[statements[0]] = statements[1]
            else:
                print("\nInvalidRuleException - Parenthesis are not balanced ==> "+rule
                        +". Therefore discarding it.\n")
                self.rules.remove(rule)

    def isValid(self, statement):
        summary = {}
        stack = []
        for index, entry in enumerate(statement):
            if(entry=="("):
                stack.append(index)
            elif(entry==")"):
                try:
                    position = stack.pop()
                    summary[position] = index
                except IndexError:
                    return False
        return not stack

    def solve(self, f1,op,f2):
        if(op==AND):
            return f1 in self.facts and f2 in self.facts
        elif(op==OR):
            return f1 in self.facts or f2 in self.facts
        else:
            return False

    def verifyPremisse(self, p):
        premisse, conclusion = p.split(ENT_SEPARATOR)
        if(self.isValid(premisse)):
            stack = list()
            solution_stack = list()
            result = False

            for i in premisse:
                print("CURRENTLY IN "+i+" FROM "+premisse +"\nstack state "+ str(stack))
                if(i != ")"):
                    if(i !="("):
                        print("=======APPEDING "+i+"=========")
                        stack.append(i)
                else:
                    f2 = stack.pop()
                    op = stack.pop()
                    f1 = stack.pop()
                    result = self.solve(f1,op,f2)
                    stack.append(result)
                    print("=======Processed %s %s %s =========" %(f1,op,f2))

                    if(result):
                        if(not isinstance(f1, bool) and f1 in self.facts and f1 not in self.queue):
                            solution_stack.append(f1)
                        if(not isinstance(f2, bool) and f2 in self.facts):
                            solution_stack.append(f2)

            if(result):
                for item in solution_stack:
                    self.queue.append(item)
                self.facts.add(conclusion)
            return result

    def buildHigherPremisse(self, target, rule=None):
        print("Searching for target: "+target)
        for r in self.rules:
            if(r != rule):
                premisse, conclusion = r.split(ENT_SEPARATOR)
                if(target == conclusion and target not in self.facts):
                    print("====>Found a valid rule: "+r)
                    if(len(premisse)>1):
                        premisse = "("+premisse+")"
                    for i in premisse:
                        if(i != ")" and i != AND and i != OR):
                            if(i !="("):
                                if(i not in self.facts):
                                    print("\n-----------Recursively looking up for new target: "+i+"-----------\n")
                                    higher_premisse = self.buildHigherPremisse(target=i,rule=r)
                                    premisse = premisse.replace(i, higher_premisse)

                                    print(higher_premisse+" was returned and appended to "+premisse)
                    print("RETURNING UPDATED PREMISSE "+premisse)
                    return premisse
        return target


    def execute(self, target):
        for r in self.rules:
            premisse, conclusion = r.split(ENT_SEPARATOR)
            if(target == conclusion):
                self.solution = self.buildHigherPremisse(target) + "=>"+target
                result = self.verifyPremisse(self.solution)
                print(self.solution)
                if(result):
                    print("Found a solution")
                    break


raw_rules = input("Enter the rules separated by semi colon\n") # ((p&q)#r)#(s&t)=>c;g#h=>x;s&(c#j)=>h
raw_facts = input("Enter the facts\n") # s, t
target = input("Enter the target: ") # x

bc = Backwards(raw_rules=raw_rules, raw_facts=raw_facts)
solution = bc.execute(target)
