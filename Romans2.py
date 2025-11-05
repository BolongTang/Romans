import Laws
# General Framework (Program)

# To some degree are still doing it. 
# Outwardly saying it's wrong, and know they're wrong, 
# But they're not repenting of these things themselves. 
# (Impetinent heart)

class Law():
    # Each set of laws has a name. 
    # A pre-defined catgory such as "Biblical" will be used if the name is reserved. 
    def __init__(self, name):
        # The name for this particular Law() object (set of laws)
        self.name = name
        # Add support for more names (predefined templates)
        if name == "Biblical":
            # TODO: Contain more than the 10 commandments. 
            # Jewish 613 laws? The oral Torah? 
            self.contents = Laws.BIBLICAL
        
        # If no reserved name is specified, initialize an empty dictionary to hold custom laws
        else: 
             self.contents = dict()

    # person is a Person() object, 
    # the only relevant attribute is: person.log
    
    # Updates a person's righteousness status according to the current law. 
    # Arguments: Reference first (which is the law itself), the thing being judged second
    # print_report prints a violation report of a person against a specific law TODO: write this into a separate file
    def check_against(self, person, print_report = False, print_test = False):
        
        violations = []

        # Initialize as True because it's custom to assume innocence
        person.righteous[self.name] = True
        # person.log is a list of tuples (time, action)
        # If any action of the person violates any law, then unrighteous
        for action in person.log.values():
             
             # TODO: provide specific violation feedbacks using law_name: law_content format. 
             for law_name, law_content in self.contents.items():
                # O(N^2) bec one for loop inside another
                # Each Law() object can only check if a person violates itself, not 
                if self.violates(law_content, action):
                    if print_report:
                        violations.append([law_name, law_content, action])
                    # TODO: Different variables for righteousness according to different sets of laws
                    # Currently only have one variable

                    # According to the current set of laws, the person is not righteous. 
                    # Ex. person.righteous["Biblical"] = False

                    # If no violation, person.righteous[self.name] will stay True. 
                    # If any violation, person.righteous[self.name] will be False onward. 
                    # Stored True only when both are True
                    person.righteous[self.name] = person.righteous[self.name] and False
        
        # According to the current set of laws, no violation, declared innocent (righteous), no change of status
        self.check_hypocrisy(person)

        if print_test:
            return self.print_report(person, violations, print_test)
        
        if print_report: 
            self.print_report(person, violations, print_test)
    
    def print_report(self, person, violations, print_test):
        if print_test: 
            report = f'According to the Law named {self.name}, {person.name} has violated:' 
            for violation in violations:
                report += f'\n{violation[0]}: {violation[1]} because {person.name} did {violation[2]}.'
            return report
        else: 
            print(f'According to the Law named {self.name}, {person.name} has violated:')
            for violation in violations:
                law_name = violation[0]
                law_content = violation[1]
                action = violation[2]
                # action is in the present tense
                print(f'{law_name}: {law_content} because {person.name} did {action}.')

    # Updates a Person's hypocrite status according to the current law. 
    def check_hypocrisy(self, person):
        # Check hypocrisy status
        # If person does not know law
        # Covered all four possible cases of the (knows_law, righteous) combination: TT, TF, FT, FF 
        if not person.knows_law: # Covers FT and FF
            # Cannot be a hypocrite by definition because there is no internal reference against which hypocrisy can form
            person.hypocrite[self.name] = False
        # if person knows law and person is righteous according to this current Law:
        elif person.knows_law and person.righteous[self.name]: # Covers TT
            # The person is not a hypocrite according to this current Law
            person.hypocrite[self.name] = False
        # else if person knows law and person is not righteous according to this current Law:
        elif person.knows_law and not person.righteous[self.name]: # Covers TF
            # The person is a hypocrite according to this current Law 
            person.hypocrite[self.name] = True
        # Branch for testing, shouldn't be activated
        else:
            print("Uncaptured hypocrisy case")

    def violates(self, law, action): 
        # HARD to decide in general. Need human judgement. For experimental automation, use unbiased LLM. 
        # If action contradicts with law, 
        # Then action violates the law
        # For each type of law there is a different way of measuring
        # Such as "T/F", numerical deviance (Ex. keeping Sabbath), or?

        # Implementing a primitive checking method for demo. (check unit test TestBiblicalRighteous1)
        # Assume action == "murder"
        # law == "You shall not murder."
        # "shall not " + "murder" == "shall not murder"
        # "shall not murder" in law == True
        # Thus the person violated the law
        if "shall not " + action in law:
            return True

# A person has a track record, and can judge
# "For in passing judgement on another you condemn yourself"
class Person():
    # log empty means newborn
    # log of a person can be imported from another file, in the format of a JSON object
    # TODO: Use the knows_law variable
    def __init__(self, name, log = dict(), knows_law = False):
        self.name = name
        # Track record, shows 
        # Person.log is a list of tuples (time, action)
        # action should have a standard format, such as being in the present tense
        self.log = log
        # Know law or not (need to be customized to each individual law)
        self.knows_law = knows_law

        # Righteous or Unrighteous
        # The default is False for practical purpose (everyone except Jesus sins)
        # Was True pre-forbidden fruit
        # person (since everyone sins)
        # Default None because to be determined later. (same below)
        
        # Implemented as a dictionary because different sets of laws test out 
        # different righteousness statuses
        # Ex. Biblical law judges one unrighteous but city law judges one righteous
        # Ex. self.righteous == {"Biblical": False, "Federal_law": True, "Austin_law": True}
        self.righteous = dict()
        # Hypocrite or not. 
        
        # many may not have the law until later in life. 
        # Each righteousness standard corresponds to exactly one hypocrite status
        # If knowing law but violating it, then hypocrite. 
        # Ex. self.hypocrite == {"Biblical": True, "Federal_law": False, "Austin_law": False}
        self.hypocrite = dict()

        # Ex. self.hypocrite == {"Biblical": False, "Federal_law": True, "Austin_law": True}
        # This is not equivalent to self.righteous
        # You may turn disobedient but still retain your righteousness status for a while
        # if you're not being checked continuously against the laws
        # Not a useful metric yet. TODO: implement this. 
        self.obedient = dict()

        # TODO: add a Perception() class shows a person's self-perception of righteous, hypocrite, obedient, etc. 
        # add a Actual() class shows a person's actual status according to the Bible
        # use a distance metric to measure the difference between self.Perception() and self.Actual()

    # self is the person
    # another is another Person() object
    # judge() uses a person's understanding of the law
    # law is a Law() object, the reference with which the Person judges
    # TODO: modifies a Perception() object
    # TODO: If another is None, one can self-judge to see where they're at
    # Ex. Suppose a Person() called Joseph judges with the Biblical Law. 
    # Ex. judge(law, another = None)
    def judge(self, law, another = None):
        # Always check oneself first
        
        # Self-judge based on the given set of laws.
        # Check against the law the literal self of the Person.
        # righteousness status and hypocrisy status (dictionary entries) 
        # of this Person() will be updated on the Law() side
        # Ex. Suppose a person has no righteousness status. 
        # Ex. self.righteous == {}
        law.check_against(self)
        # Ex. Now the person has a righeousness status according to the Biblical Law. 
        # Ex. self.righteous == {"Biblical": False}

        # If there is another to judge, then judge. 
        if another != None:
            law.check_against(another)

        # For each entry action in self.log which is 
        # self, log is a tuple in self.log. Tuple used so each record is immutable. 
        # TODO: Make existing self.log immmutable.

# No one has excuse. (Ch1)
# Salvation decision makes no difference whether you have the law or not. 
# However, Paul says: to those who know the law, (Ch2)

# You think knowing the law is enough, doing it, storing up wrath for yourself. (v5)

# If you are saved, do you still get some sort of punishment in heaven for unrepented sin? 
# You need to be intentionally 
# Consequences of sin; less treasure in heaven; (relationship, fellowship)

# 

# Particular Instance (Test Case)
# Therefore you have no excuse, o man, every one of you who judges. 
# , because you, the judge, practice the very same things.

# Ch2 (immortality (things that are immortal?), no partiality (order doesn't change))

# Why does someone gets judged 

# If you can be saved by doing the best you can, then the Great Commission doesn't make sense. 
# Bad conclusion: Paul said: if no law, sin lays dead. 
# 

# Being God's people is marked in heart, and not a physical thing. 

# Some denominations do baptism, like the new circumcision. 
# Like RC Sproul. But God's people are marked physically. 

# Reformed Presbytarian infant baptism positions? 