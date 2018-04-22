import re

RULE_SEPARATOR = ";"
ENT_SEPARATOR = "=>"
AND = "&"
OR = "#"

class Forward(object):

    def __init__(self, raw_facts, raw_rules, target):
        self.facts = raw_facts
        self.rules = raw_rules
        self.entailments = {}
        self.target = target
        self.queue = list()

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

        # for key in entailments:
        #     print("The statement "+key+" entails in "+entailments[key])

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
        if(len(premisse) > 1):
            premisse = "("+premisse+")"

        stack = list()
        solution_stack = list()
        result = False
        # print("\nEVALUATING THE PREMISSE --> "+p)
        # print(premisse)
        for i in premisse:
            if(i != ")"):
                if(i !="("):
                    stack.append(i)
            else:
                f2 = stack.pop()
                op = stack.pop()
                f1 = stack.pop()
                result = self.solve(f1,op,f2)
                # print(str(f1)+str(op)+str(f2)+" = "+str(result))
                stack.append(result)

                if(result):
                    if(not isinstance(f1, bool) and f1 in self.facts and f1 not in self.queue):
                        solution_stack.append(f1)
                        # print("\n------------Adding "+str(f1)+" as a TEMP step to SOLUTION-------\n")
                    if(not isinstance(f2, bool) and f2 in self.facts):
                        solution_stack.append(f2)
                        # print("\n------------Adding "+str(f2)+" as a TEMP step to SOLUTION-------\n")

        if(result):
            for item in solution_stack:
                self.queue.append(item)
            self.rules.remove(p)
            # print("\n------------Adding "+str(conclusion)+" as fact-------\n")
            self.facts.add(conclusion)
        return result

    def execute(self):
        count = 0
        while((len(self.rules) > 0 or (self.target not in self.facts)) and count < 10):
            # print(" ===There are "+str(len(self.rules))+" rules left to process====")
            # for rule in self.rules:
            #     print("    >>"+rule)
            for r in self.rules:
                res = self.verifyPremisse(r)
                # print("THIS PREMISSE IS "+str(res))
                # var = ", ".join(str(f) for f in (self.facts))
                # print(var+"\n\n\n")
                # print(" ===There are "+str(len(self.rules))+" rules left to process====")
                # for rule in self.rules:
                #     print("    >>"+rule)
            count+=1
            # print("====THIS ROUND HAS FINISHED====")
            # print("====== NUM OF ITERATIONS: "+str(count))
        return self.target in self.facts


raw_rules = input("Enter the rules separated by semi colon\n")
raw_facts = input("Enter the facts\n")
target = input("Enter the target: ")

fc = Forward(raw_rules=raw_rules, raw_facts=raw_facts, target=target)
solution = fc.execute()
if(solution):
    tmp = " => ".join(fc.queue)
    print("It is possible to achieve solution through "+tmp)
else:
    print("Impossible to achieve solution")
