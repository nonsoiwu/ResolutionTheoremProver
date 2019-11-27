#Project 2 - CISC481
#University of Delaware
#Author: Nonso Iwu
#Resolution Theorem-prover

import copy

#===========================================================================
#                               HELPER FUNCTIONS
#===========================================================================
def typeCheck(obj, typeObj, message):
    """
    Simple function for checking if an object is of a certain type

    Checks if obj is the same type as typeObj, if not, it will raise
        an exception with the message parameter
    """
    if type(message) != type(""):
        raise Exception('message not of type \'string\'')
    if type(obj) != type(typeObj):
        raise Exception(message)
    
#1. Resolution Theorem Proving

"""
-RTP (Resolution Theorem Prover)
-Takes in a number of Axioms in clausal form
-Takes in a negated theorem
-Attempts to derive the '/0' clause

-Horn Clauses:
    P <= (P1 and P2 and P3 and ... and Pn),
    which is equivalent to (P or notP1 or notP2 notP3 or ... or notPn)
"""

#2. Your Theorem-Prover

"""
Axioms are Horn Clauses
Horn Clauses:
    Will be coded as a list of predicates:
    First predicate will be non-negated
    Rest of the predicates will be assumed negated
Goal Clause:
    List of predicates.
    Assumed negated.

Predicate will be represented as a list
    First element: name
    Remainnig elements: 0 | Constant | Var Names

Var Names begin with ?
Constants do not
"""

#===========================================================================
#                               pELEMENT CLASS
#===========================================================================

class pElement:
    """
    Elements for a Predicate class's 'elements' list
    Attributes:
        name (string), the name of the predicate
        group (string):
            if "z", it is zero
            if "c", it is a constant (Default)
            if "?", it is a variable
    """
    def __init__(self):
        self.name = ""
        self.group = "c"
        self.unique = 0
        self.negated = False

    def setAttributes(self, name, group):
        """
        Explicitly sets variables for pElement class
        param:
            'name' (string) the name of this pElement
            'group' (string) the classification of this pElement
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(name, "", "parameter 'name' is not of type string")
        typeCheck(group, "", "parameter 'group' is not of type string")
        if(group != "c" and group != "z" and group != "?"):
            print("parameter 'group' has to be a 'z', 'c', or '?'")
            return None
        self.group = group
        self.name = name
        return self

    def toString(self):
        """
        Returns a readable string to identify the pElement class
        Examples (class instance in the form (name, group, unique, negated)):
            ("ex", "?", "0", False) => ?ex
            ("ex", "c", "0", False) => ex
            ("ex", "z", "0", False) => 0
            ("ex", "?", "0", True)  => ~ex
            ("ex", "?", "1", True)  => ~ex.1
        returns:
            (string) a string in the form shown above 
        """
        return {True:"~"}.get(self.negated,"") + {"?":"?"}.get(self.group,"") + {"z":"0"}.get(self.group, self.name) + {0:""}.get(self.unique, "."+str(self.unique))

    def createUnique(self, uniqueNum):
        """
        Initializes a pElement and creates a uniquified version
        of it using 'uniqueNum'
        param:
            'uniqueNum' (int)
        returns:
            a pElement class with attributes identical to the one
                calling the method, with its unique attribute set to 'uniqueNum' 
        """
        typeCheck(uniqueNum, 1, "parameter 'uniqueNum' is not of type int")
        p = pElement()
        p.setAttributes(self.name, self.group).unique = uniqueNum
        p.negated = self.negated
        return p
                                                                                                
    def negate(self):
        """
        Sets the negated attribute to the opposite of its value
        returns:
            self (the instance of the class that calls method)
        """
        self.negated = not self.negated 
        return self
 
    def equals(self, oE):
        """
        Equates two pElement classes
        returns:
            True if all attributes within both classes are the same,
            False otherwise
        """
        return self.name==oE.name and self.group==oE.group and self.unique==oE.unique and self.negated==oE.negated

    def clone(self):
        """
        Clones this instance of pElement class
        returns:
            New cloned pElement class from calling class
        """
        newE = pElement()
        newE.name = self.name
        newE.group = self.group
        newE.unique = self.unique
        newE.negated = self.negated
        return newE

#===========================================================================
#                               PREDICATE CLASS
#===========================================================================

class Predicate:
    """
    Predicate class for the Axiom class
    Attributes:
        name (string), the name of the predicate
        elements (list), this is a list of pElement objects
    """

    def __init__(self):
        self.name = ""
        self.elements = []
        self.negated = False

    def setAttributes(self, name, elements):
        """
        Explicitly sets variables for Predicate class
        param:
            'name' (string) the name of this Predicate
            'elements' (list) a list of pElements
        returns:
            self (the instance of the class that calls method)
        """
        dummy = pElement()
        typeCheck(name, "", "parameter 'name' is not of type string")
        self.name = name
        for e in elements:
            typeCheck(e, dummy, "elements has to be a list of 'pElement' Objects")
            self.elements.append(e.clone())
        return self

    def addElement(self, pE):
        """
        Appends pElement 'pE' into the elements list attribute
        param:
            'pE' (pElement) the pElement to be added
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(pE, pElement(), "parameter 'pE' is not of type pElement")
        self.elements.append(pE.clone())
        return self

    def toString(self):
        """
        Returns a readable string to identify the Predicate class
        Examples (class instance in the form (name, elements, negated)):
            ("ex", [pE1, pE2...], False) => (ex pE1.toString() ... )
            ("ex", [pE1, pE2...], True)  => ~(ex pE2.toString() ... )
        returns:
            (string) in the form shown above
        """
        temp = "(" + self.name
        for p in self.elements:
            temp += " " + p.toString()
        return {True:"~"}.get(self.negated,"")+temp + ")"
    
    def negate(self):
        """
        Sets the negated attribute to the opposite of its value
        returns:
            self (the instance of the class that calls method)
        """
        self.negated = not self.negated
        return self

    def equals(self, otherPred):
        """
        Equates two Predicate classes
        param:
            otherPred (Predicate) predicate to be compared
        returns:
            True if all attributes within both classes are the same,
            False otherwise
        """
        if(len(self.elements)!=len(oE.elements)):
            return False
        
        for i in range(len(self.elements)):
            if(not self.elements[i].equals(oE.elements[i])):
               return False
               
        return self.name==otherPred.name and self.negated==otherPred.negated

    def clone(self):
        """
        Clones this instance of Predicate class
        returns:
            New cloned Predicate class from calling class
        """
        newP = Predicate()
        newP.name = self.name
        for e in self.elements:
            newE = e.createUnique(e.unique)
            newP.addElement(newE)
        newP.negated = self.negated
        return newP

#===========================================================================
#                               AXIOM CLASS
#===========================================================================

class Axiom:
    """
    Axiom object for the Theorem-Prover
    Attributes:
        predicates (list), this is a list of Predicate objects
        
    First predicate will be non-negated
    Rest of the predicates will be assumed negated
    """

    def __init__(self):
        self.predicates = []

    def setAttributes(self, predicates):
        """
        Explicitly sets variables for Axiom class.
        param:
            'predicates' (list) of Predicates for this Axiom class
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(predicates, [], "predicates has to be a list of 'Predicate' Objects")
        dummy = Predicate()
        for p in predicates:
            typeCheck(p, dummy, "predicates has to be a list of 'Predicate' Objects")
            self.predicates.append(p.clone())
        self.hornify()
        return self

    def addPredicate(self, pred):
        """
        Appends Predicate 'pred' into the predicate list attribute
        param:
            'pred' (Predicate) the pred to be added
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(pred, Predicate(), "pred is not of type 'Predicate'")
        self.predicates.append(pred.clone())
        self.hornify()
        return self

    def hornify(self):
        """
        Makes this Axiom a horn clause.
        i.e. the first Predicate in the predicates list non-negated while 
            the rest are negated
        param:
            None
        returns:
            self (the instance of the class that calls method)
        """
        #Abort if no Predicates in list
        if len(self.predicates) != 0:
            first = True
            for p in self.predicates:
                if(first):
                    p.negated = False
                    first = False
                else:
                    p.negated = True
                    
        return self
    
    def toString(self):
        """
        Returns a readable string to identify the Axiom class
        Example (class instance in the form [predicates]):
            [pr1, pr2...] => (pr1.toString(), pr2.toString() ... )
        returns:
            (string) in the form shown above
        """
        if len(self.predicates) == 0:
            return "( )"

        temp = "("
        for p in self.predicates:
            temp += p.toString() + " "
            
        return temp[:-1]+")"

    def clone(self):
        """
        Clones this instance of Axiom class
        returns:
            New cloned Axiom class from calling class
        """
        newA = Axiom()
        for p in self.predicates:
            newA.predicates.append(p.clone())
        return newA

    def merge(self, oAxiom):
        """
        Takes the predicats of an Axiom class and adds them to the
            list of predicates of the calling Axiom class
        param:
            oAxiom (Axiom) the other Axiom to be merged
                oAxiom is left unchanged
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(oAxiom, Axiom(), "oAxiom is not of type 'Axiom'")
        copyA = oAxiom.clone()
        for p in oAxiom.predicates:
            self.predicates.append(p)
        return self
        
    def negate(self):
        """
        Sets the negated attribute or each predicate in predicates list
            to the opposite of its value
        returns:
            self (the instance of the class that calls method)
        """
        for p in self.predicates:
            p.negate()
        return self

#===========================================================================
#                               THEOREM CLASS
#===========================================================================

class Theorem:
    """
    The Theorem-Prover class
    Attributes:
        goals (list), a list of Axiom objects
        premises (list), a list of Axiom objects
        searchType (boolean), indicator for how openList will be searched
            True:  Breadth First Search (openList implements Queue)
            False: Depth First Search   (openList implements Stack)
    """

    def __init__(self, searchType=False):
        typeCheck(searchType, True, "sT is not of type 'boolean'")
        self.goals = []
        self.premises = []
        self.searchType = searchType

    def setAttributes(self, goals, premises):
        """
        Explicitly sets variables for Theorem class.
        param:
            'goals' (list) of Axiom classes for the goals attribute of Theorem class
            'premises' (list) of Axiom classes for the premises attribute of Theorem class
        returns:
            self (the instance of the class that calls method)
        """
        dummy = Axiom()
        typeCheck(goals, [], "goals is not of type 'list'")
        typeCheck(premises, [], "premises is not of type 'list'")
        for g in goals:
            typeCheck(g, dummy, "goals has to be a list of 'Axiom' Objects")
            self.goals.append(g.clone().negate())
        for p in premises:
            typeCheck(p, dummy, "premises has to be a list of 'Axiom' Objects")
            self.premises.append(p.clone())
        return self

    def setSearch(self, sT):
        """
        Sets the search method for the Theorem class.
        param:
            'sT' (boolean) indicates which search type to use for Theorem.prove()
                True: Breadth First Search (openList implements Queue)
                False: Depth First Search  (openList implements Stack)
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(sT, True, "sT is not of type 'boolean'")
        self.searchType = sT
        return self
        
    def addGoal(self, ax):
        """
        Adds an Axiom class to the 'goals' attribute of this Theorem class
        param:
            ax (Axiom) Axiom to be added to the goals list
        return:
            self (the instance of the class that calls method)
        """
        typeCheck(ax, Axiom(), "ax is not of type 'Axiom'")
        self.goals.append(ax.clone().negate())
        return self

    def addPremise(self, ax):
        """
        Adds an Axiom class to the 'premises' attribute of this Theorem class
        param:
            ax (Axiom) Axiom to be added to the premises list
        return:
            self (the instance of the class that calls method)
        """
        typeCheck(ax, Axiom(), "ax is not of type 'Axiom'")
        self.premises.append(ax.clone())
        return self

    def uniquifyPremises(self):
        newPrem = []
        uniB = bindDict()
        dummy = pElement().setAttributes("dummy", "z")
        
        for ax in self.premises:
            newAx = uniquify(ax, uniB)
            newPrem.append(newAx)
        return newPrem
    
    def prove(self, iters=300):
        """
        Resolves the goal clauses in the 'goals' attribute to the clauses in
        the 'premises' attribute (Knowledge Base)
        This function will print:
            Iteration Count
            Predicate Comparisons
            Results:
                goal clauses and their bindings
        param:
            ?iters (int) the amount of iterations that the prove() function
                will search through successor clauses from the Open List.
                Default is 300 iterations
        returns
            a list of bindDict classes that correspond to the solutions for
            the Theorem solver
        """
        typeCheck(iters, 2, "iters is not of type 'int'")

        #Show theorem:
        self.show()

        print()
        print("Search Method:", {True:"Breadth",False:"Depth"}.get(self.searchType, ""), "First Search")
    
        #Class definition of Open List for the solver
        #Only exists within the scope of the prove() function
        class openList:
            def __init__(self):
                self.data = []

            def push(self, element):
                self.data.append(element)

            def popQueue(self):
                d = self.data.pop(0)
                return d

            def popStack(self):
                d = self.data.pop()
                return d

            def getLength(self):
                return len(self.data)

            def isEmpty(self):
                return len(self.data)==0
            
            def show(self):
                for d in self.data:
                    print(d[0].toString())

        #Create openList
        oL = openList()
        #Fill openList with all goal clauses
        for g in self.goals:
            #Add the axiom and its associated bindings
            #Tuple of (axiom, bindDict)
            oL.push((g , bindDict()))

        #Create bindDict as list of bindings
        bindings = bindDict()
        
        iteration = -1
        oLNode = -1
        solutions = []
        #Cease after max iteration count
        for i in range(iters):
            iteration = i + 1
            if oL.isEmpty():
                #Open List is empty so algorithm halts
                break
            
            #print()
            #print("===Iteration "+str(iteration)+"===")
            #print("Open List:")
            #oL.show()
            
            #Retrieve clause from open list
            if self.searchType == False:
                #Depth First Search
                oLNode = oL.popStack()
            else:
                #Breadth First Search
                oLNode = oL.popQueue()
            
            #Clean up Node references
            oLClause = oLNode[0]
            oLBD = oLNode[1]

            for ax in self.premises:
                #Check if predicates are able to be unified
                if ax.predicates[0].name == oLClause.predicates[0].name:
                    if ax.predicates[0].negated != oLClause.predicates[0].negated:
                        #UNIQUIFY HERE
                        prem = uniquify(ax, oLBD)

                        #print()
                        #print("Compare:")
                        #print(oLClause.toString())
                        #print(prem.toString())
                        
                        #UNIFY HERE
                        #tBD = unify(oLClause.predicates[0], prem.predicates[0], oLBD, True)
                        tBD = unify(oLClause.predicates[0], prem.predicates[0], oLBD, False)
                        
                        if tBD != None:

                            #Pop first predicate off of KB clause
                            prem.predicates.pop(0)
                            
                            #Pop first predicate off of openList clause
                            #Copy the clause so we are not working directly on it
                            oLcopy = oLClause.clone()
                            oLcopy.predicates.pop(0)

                            #MERGE THE PREMISE CLAUSE TO THE OPEN LIST CLAUSE
                            #THIS ORDER IS IMPORTANT
                            oLcopy.merge(prem)
        
                            #Check to see if empty clause was created
                            if len(oLcopy.predicates) == 0:
                                if(tBD.isEmpty()):
                                    #Add the old bindings since tBD is empty
                                    solutions.append(oLBD)
                                else:
                                    solutions.append(tBD)
                                continue
                            
                            #CHASE bindings of new vars
                            chasedAxioms = chasify(oLcopy, tBD)
                            #Place new merged axioms in open List
                            for c in chasedAxioms:
                                oL.push((c,tBD))

        #Report findings
        print()
        print("===Results===")
        print("Iterations:", iteration)
        print()
        
        if(len(solutions) == 0):
            print("No Solutions.")

        for g in self.goals:
            print(g.toString()+":")
            sCt = 1
            for s in solutions:
                print(str(sCt)+":"+readVariableBindings(g,s))
                sCt += 1
        
        return solutions

    def show(self):
        """
        Prints the contents of the Theorem attributes.
        returns:
            None
        """
        print("Premises:")
        for p in self.premises:
            print(p.toString())
        print()
        print("Goals:")
        for g in self.goals:
            print(g.toString())

#3. A Simpliﬁed Example: Seeing it as Graph Search

#4. Some Functions You Should Write

#===========================================================================
#                               BIND DICTIONARY CLASS
#===========================================================================

class bindDict:
    """
    This will be the class that will represent a list of bindings.
    The reason why this will substitute for a list of bindings is for
        speed of retrieving bindings of a pElement.

    A bindDict uses a dictionary {} to keep track of the index that the
        bindings of a variable is kept in a list.

    A tuple is created from a pElement, then that tuple is fed to the
        dictionary as a key. The value of that key will be the index in the
        values attribute where the bindings of that pElement. At that
        index, there is another tuple that holds a reference of the pELement
        that was hashed, and a list of references to the pElements that the
        hashed pElement is bound to.
    
    Attributes:
        keys (dictionary) of hashed pElement class information which map to
            the index of its entry in the value attribute
        values (list) of tuples in the form of (key, bindings)
    """
    
    def __init__(self):
        self.keys = {}
        self.values = []

    def identify(self, pElem):
        """
        Creates a hashabe tuple object from the attributes of pElem
        param:
            pElem (pElement) the pElement class to be hashed
        returns:
            a tuple containing the name, group, unique, and negated
                attributes of a pElement class
        """
        typeCheck(pElem, pElement(), "param 'pElem' not of type pElement")
        return (pElem.name, pElem.group, pElem.unique, pElem.negated)
        
    def get(self, key):
        """
        Retrieves the bindings of a pElement
        param:
            key (pElement) the pElement that is to be assessed for its
                bindings
        returns:
            A list of pElements that the 'key' is bound to
            Returns None if there is no entry for 'key' in the bindDict
        """
        typeCheck(key, pElement(), "param 'key' not of type pElement")
        i = self.identify(key)
        f = self.keys.get(self.identify(key), -1)
        if f == -1:
            return None
        else:
            return self.values[f][1]

    def getLowest(self, key):
        """
        Retrieves the chased bindings of a pElement
        This function will continually call bindDict.get() in order to
            get the chased bindings for a pElement.
        If a pElement is bound to more than one other pElements, the chased
            bindings of those pElements will be retrieved instead
        For example:
            x -> y
            x -> z
            y -> 1
            z -> 4
            A call to getLowest(x) will retrieve [1 4]
        param:
            key (pElement) the pElement that is to be assessed for its
                bindings
        returns:
            A list of the lowest level pElements that the 'key' is bound to
            Returns None if there is no entry for 'key' in the bindDict
        """
        typeCheck(key, pElement(), "param 'key' not of type pElement")
        #BFS Search for bindings of a variable
        queue = [key]
        final = []
        while len(queue) > 0:
            elem = queue.pop(0)
            binds = self.get(elem)
            if binds == None:
                #No entry of elem
                return None
            elif binds == []:
                #Found a pElement with no bindings
                final.append(elem)
            else:
                #Found a pElement with bindings
                for e in binds:
                    if e.group != "?":
                        final.append(e)
                    else:
                        queue.append(e)
        return final
            
    def add(self, key, value):
        """
        Adds a binding to the bindDict from key => value
        This will also create an empty entry for the value within
            the bindDict values list attribute
        param:
            key (pElement) the pElement to be hashed
            value (pElement) the pElement to be bound to key
        returns:
            self (the instance of the class that calls method)
        """
        typeCheck(key, pElement(), "param 'key' not of type pElement")
        typeCheck(value, pElement(), "param 'value' not of type pElement")

        #Abort if same thing
        if(key.equals(value)):
            return self

        #Abort if...
        if (key.group != "?") and (value.group != "?"):
            if(value.group != "?"):
                #both key and value are constants or zeroes
                raise KeyError("Key and Value are both non-variables.")
            else:
                #key is a constant or zero
                raise KeyError("Key is a non-variable.")

        #Abort if value is already bound to key
        if(self.isBound(key, value)):
            return self
        
        #Check attributes of key and value
        if key.group == "?" and value.group == "?":

            #Both key and value are variables
            ind = len(self.values)
            if not self.exists(key):
                #Key entry doesnt exist
                self.keys[self.identify(key)] = ind
                self.values.append((key,[]))
                ind += 1

            if not self.exists(value):
                #Value entry does not exist
                self.keys[self.identify(value)] = ind
                self.values.append((value,[]))

            keyBinds = self.get(key)
            keyBinds.append(value)
            
        else:
                            
            #Value is a constant/zero
            if not self.exists(key):
                #Key entry doesnt exist
                self.keys[self.identify(key)] = len(self.values)
                self.values.append((key,[]))

            keyBinds = self.get(key)
            keyBinds.append(value)
                        
        return self

    def isBound(self, key, value):
        """
        Checks if value is bound to key
        params:
            key (pElement) the pElement to be looked into
            value (pElement) the pElement to be searched for
        returns:
            True if value appears within the key's bindings
            False otherwise
        """
        typeCheck(key, pElement(), "param 'key' not of type pElement")
        typeCheck(value, pElement(), "param 'value' not of type pElement")

        val = self.get(key)
        if val == None:
            return False
        for b in val:
            if b.equals(value):
                return True
        return False

    def exists(self, key):
        """
        Checks if key has an entry within the bindDict
        params:
            key (pElement) the pElement to be assessed
        returns:
            True if there is an entry of key in the bindDict
            False otherwise
        """
        typeCheck(key, pElement(), "param 'key' not of type pElement")
        i = self.identify(key)
        f = self.keys.get(self.identify(key), -1)
        if f == -1:
            return False
        return True
                
    def show(self):
        """
        Prints the bindings of the bindDict.
        returns:
            None
        """
        if len(self.values)==0:
            print("[]")
            
        for v in self.values:
            for b in v[1]:
                print(v[0].toString() + " -> " + b.toString())

    def isEmpty(self):
        """
        Checks if the calling bindDict has no bindings
        returns:
            True if values attribute is empty
            False otherwise
        """
        return len(self.values) == 0

#===========================================================================
#                           THEOREM HELPER FUNCTIONS
#===========================================================================

def readBindings(bindings):
    """
    Reads the bindings of a bindDict
    returns:
        None
    """
    if(bindings == None):
        print(None)
        return None
    typeCheck(bindings, bindDict(), "param 'bindings' not of type bindDict()")
    bindings.show()
    
def unify(pred1, pred2, bindings, showNew=False):
    """
    Unifies the variables of one Predicate and another Predicate
    param:
        pred1 (Predicate) predicate to be unified
        pred2 (Predicate) predicate to be unified
        bindings (bindDict) collection of bindings to reference during unification
        showNew (boolean) indicates whether or not the function will
            print new bindings:
                True, will show
                False, will not show
    returns:
        None, if unification failed
            -pred1 and pred2 names are not equal
            -pred1 and pred2 element lengths are not equal
            -Comparison of to unequal constants
        Empty bindDict, if no additional bindings were needed (success)
        New bindDict, if additional bindings were needed (success)
            -Includes the new and previous bindings
    """
    typeCheck(pred1, Predicate(), "param 'pred1' not of type Predicate")
    typeCheck(pred2, Predicate(), "param 'pred2' not of type Predicate")
    typeCheck(bindings, bindDict(), "param 'bindings' not of type bindDict")
    foundBindings = False
    nB = []
    newBinds = copy.deepcopy(bindings)
    comp1 = None
    comp2 = None
    
    #Abort if predicate names are not the same
    if pred1.name != pred2.name:
        return None

    #Abort if predicate element sizes are not equal
    if len(pred1.elements) != len(pred2.elements):
        return None
        
    #Check bindings
    for j in range(len(pred1.elements)):
        comp1 = pred1.elements[j]
        comp2 = pred2.elements[j]
                      
        #Check if same predicate vars
        if comp1.equals(comp2):
            continue

        #Check if 2 constants/zeroes are being compared
        if (comp1.group != "?") and (comp2.group != "?"):
            return None

        #Check if both compares are variables
        if comp1.group == "?" and comp2.group == "?":
            #Add to bindings
            #Binding Dictionary handles binding
            newBinds.add(comp1, comp2)
            foundBindings = True
            if(showNew):
                nB.append(comp1.toString()+" -> "+comp2.toString())

        #Check if comp1 is the non variable
        elif comp1.group != "?":
            #Check if comp2 is bound to a constant
            #Left way binding
            newBinds.add(comp2, comp1)
            foundBindings = True
            if(showNew):
                nB.append(comp2.toString()+" -> "+comp1.toString())

        else:
            #Comp2 is the non variable
            newBinds.add(comp1, comp2)
            foundBindings = True
            if(showNew):
                nB.append(comp1.toString()+" -> "+comp2.toString())

    if foundBindings == True:
        if showNew:
            print("New Bindings:")
            for s in nB:
                print(s)
        return newBinds
    if showNew:
        print("New Bindings:\nNone.")
    return bindDict()

def binding(var, bindings):
    """
    Chases a binding through transitive bindings
    See the bindDict.getLowest() for implementation
    param:
        var (pElement) the pElement to be chased
        bindings (bindDict) the collection of bindings to use for chasing
    returns:
        simply calls bindDict.getLowest(var)
    """
    typeCheck(var, pElement(), "param 'var' not of type pElement")
    typeCheck(bindings, bindDict(), "param, 'bindings' not of type bindDict")
    return bindings.getLowest(var)

def readVariableBindings(clause, bindings):
    """
    Reads lowest transitive bindings of a variable in an Axiom.
    param:
        clause (Axiom) the Axiom to be read from
        bindings (bindDict) the collection of bindings to use for chasing
    returns:
        None
    """
    typeCheck(clause, Axiom(), "param 'clause' not of type Axiom")
    typeCheck(bindings, bindDict(), "param 'bindings' not of type bindDict")
    explored = []
    finalstring = ""
    for p in clause.predicates:

        for e in p.elements:

            #Skip if element is not a variable
            if e.group != "?":
                continue
            
            found = False
            #Check if variable was already read
            for ex in explored:
                if(ex.equals(e)):
                    found = True
                    break
            if found:
                continue

            #Read bindings for element
            binds = binding(e, bindings)
            bstr = e.toString() + "/"
            for b in binds:
                bstr += b.toString()+"|"
            finalstring += bstr[:-1] + ", "
            
    return "{"+finalstring[:-2]+"}"
    
def chasify(clause, bindings):
    """
    Substitutes each variable in within the predicates of an Axiom class
        with its chased bindings
    For example:
        Axiom = (ex x y z)
    param:
        clause (Axiom) the Axiom to be substituted
        bindings (bindDict) the bindDict to be used for chasing
    returns:
        a list of axioms that resulted from the chasing
        Note:
            if a pElement is bound to more than one othr pElements, then
            an Axiom for each combination of those pElements will be added
            to the returned list of Axioms
            Example:
                Axiom = (ex x y z)
                Bindings:
                    x -> 3
                    x -> 4
                    y -> w
                    z -> t
                chasify(Axiom, Bindings) returns:
                    [(ex 3 w t) (ex 4 w t)]
    """
    typeCheck(clause, Axiom(), "param 'clause' not of type Axiom")
    typeCheck(bindings, bindDict(), "param, 'bindings' not of type bindDict")

    ax = clause.clone()
    final = []
    queue = [ax]
    abort = False
    while len(queue) > 0:
        #Take axiom out of queue
        a = queue.pop(0)

        #Run through predicates
        for j in range(len(clause.predicates)):
            p = a.predicates[j]

            #Run through elements
            for i in range(len(p.elements)):
                e = p.elements[i]
                newE = binding(e, bindings)
                if newE == None:
                    #pass over, no need to chase unexplored variable
                    continue
                elif len(newE) > 1:
                    #Split axioms and add to queue
                    for elem in newE:
                        newAx = a.clone()
                        newAx.predicates[j].elements[i] = elem
                        queue.append(newAx)
                    abort = True
                else:
                    #Continue with chasing, no need to split
                    p.elements[i] = newE[0]
                if abort:
                    break
            if abort:
                break
        if not abort:
            final.append(a)
        abort = False

    return final

def uniquify(clause, uniqueDict):
    """
    Creates a copy of clause with variables renamed to ones that are
        not within a bindDict
    param:
        clause (Axiom) the Axiom the be uniquified
        uniqueDict (bindDict) the collection of existing bindings
    returns:
        an Axiom with variables renamed uniquely (based on uniqueDict)
    """
    typeCheck(clause, Axiom(), "param 'clause' not of type Axiom")
    typeCheck(uniqueDict, bindDict(), "param 'uniqueDict' not of type bindDict")
    ax = Axiom()

    #Look through predicates of clause
    for p in clause.predicates:
        newp = Predicate().setAttributes(p.name,[])

        #Create unique variables for each pElement
        for e in p.elements:
            #Create copy of e
            newE = e.createUnique(e.unique)
            if e.group == "?":
                checkE = -1

                #Loop through unique numbers until one isn't taken
                while checkE != None:
                    if checkE == []:
                        break
                    checkE = uniqueDict.get(newE)
                    newE = e.createUnique(newE.unique + 1)
                    
            #Add Element to new predicate
            newp.addElement(newE)
            
        #Add new Predicate to clause
        ax.addPredicate(newp)
        
    return ax
