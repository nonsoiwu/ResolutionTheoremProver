from theorem_prover import *

#===========================================================================
#                               THEOREM SET UP
#===========================================================================

eX = pElement().setAttributes("x","?")      #?x
eY = pElement().setAttributes("y","?")      #?y
eZ = pElement().setAttributes("z","?")      #?z
eU = pElement().setAttributes("u","?")      #?u
eV = pElement().setAttributes("v","?")      #?v

"""
(defvar *premises-1*
  '(((aunt ?x ?y) (sister ?x ?z) (mother ?z ?y))
    ((aunt ?x ?y) (sister ?x ?z) (father ?z ?y))
    ((sister Mary Sue))
    ((sister Mary Doug))
    ((father Doug John))
    ((mother Sue Paul))))

(defvar *goals-1*
  '((aunt ?x ?y)))
"""
mary = pElement().setAttributes("Mary","c")
sue = pElement().setAttributes("Sue","c")
doug = pElement().setAttributes("Doug","c")
john = pElement().setAttributes("John","c")
paul = pElement().setAttributes("Paul","c")

auntv = Predicate().setAttributes("aunt", [eX, eY])
sisv = Predicate().setAttributes("sister",[eX, eZ])
sis1 = Predicate().setAttributes("sister",[mary, sue])
sis2 = Predicate().setAttributes("sister",[mary, doug])
fatherv = Predicate().setAttributes("father", [eZ, eY])
father1 = Predicate().setAttributes("father", [doug, john])
motherv = Predicate().setAttributes("mother", [eZ, eY])
mother1 = Predicate().setAttributes("mother", [sue, paul])

t1ax1 = Axiom().setAttributes([auntv, sisv, motherv])
t1ax2 = Axiom().setAttributes([auntv, sisv, fatherv])
t1ax3 = Axiom().setAttributes([sis1])
t1ax4 = Axiom().setAttributes([sis2])
t1ax5 = Axiom().setAttributes([father1])
t1ax6 = Axiom().setAttributes([mother1])
th1 = Theorem().setAttributes([Axiom().setAttributes([auntv])],[t1ax1,t1ax2,t1ax3,t1ax4,t1ax5,t1ax6])

"""
(defvar *premises-2*
  '(((simple_sentence ?x ?y ?z ?u ?v) (noun_phrase ?x ?y) (verb_phrase ?z ?u ?v))
    ((noun_phrase ?x ?y) (article ?x) (noun ?y))
    ((verb_phrase ?x ?y ?z) (verb ?x) (noun_phrase ?y ?z))
    ((article a))
    ((article the))
    ((noun man))
    ((noun dog))
    ((verb likes))
    ((verb bites))))

(defvar *goals-2*
  '((simple_sentence ?x ?y ?z ?u ?v)))
"""

ss = Predicate().setAttributes("simple_sentence", [eX, eY, eZ, eU, eV])
npv1 = Predicate().setAttributes("noun_phrase", [eX, eY])
npv2 = Predicate().setAttributes("noun_phrase", [eY, eZ])
vpv1 = Predicate().setAttributes("verb_phrase", [eZ, eU, eV])
vpv2 = Predicate().setAttributes("verb_phrase", [eX, eY, eZ])
nounv = Predicate().setAttributes("noun", [eY])
articlev = Predicate().setAttributes("article", [eX])
verbv = Predicate().setAttributes("verb", [eX])

a = Predicate().setAttributes("article", [pElement().setAttributes("a","c")])
the = Predicate().setAttributes("article", [pElement().setAttributes("the","c")])
man = Predicate().setAttributes("noun", [pElement().setAttributes("man","c")])
dog = Predicate().setAttributes("noun", [pElement().setAttributes("dog","c")])
likes = Predicate().setAttributes("verb", [pElement().setAttributes("likes","c")])
bites = Predicate().setAttributes("verb", [pElement().setAttributes("bites","c")])

t2ax1 = Axiom().setAttributes([ss, npv1, vpv1])
t2ax2 = Axiom().setAttributes([npv1, articlev, nounv])
t2ax3 = Axiom().setAttributes([vpv2, verbv, npv2])
t2ax4 = Axiom().setAttributes([a])
t2ax5 = Axiom().setAttributes([the])
t2ax6 = Axiom().setAttributes([man])
t2ax7 = Axiom().setAttributes([dog])
t2ax8 = Axiom().setAttributes([likes])
t2ax9 = Axiom().setAttributes([bites])

th2 = Theorem().setAttributes([Axiom().addPredicate(ss)],[t2ax1, t2ax2, t2ax3, t2ax4, t2ax5, t2ax6, t2ax7, t2ax8, t2ax9])

"""
(defvar *premises-3*
  '(((ancestor ?x ?y) (parent ?x ?y))
    ((ancestor ?x ?y) (ancestor ?x ?z) (parent ?z ?y))
    ((parent Mary Paul))
    ((parent Sue Mary))))

(defvar *goals-3*
  '((ancestor ?x ?y)))
"""

ancv1 = Predicate().setAttributes("ancestor", [eX, eY])
ancv2 = Predicate().setAttributes("ancestor", [eX, eZ])
parv1 = Predicate().setAttributes("parent", [eX, eY])
parv2 = Predicate().setAttributes("parent", [eZ, eY])
par1 = Predicate().setAttributes("parent", [mary, paul])
par2 = Predicate().setAttributes("parent", [sue, mary])

t3ax1 = Axiom().setAttributes([ancv1, parv1])
t3ax2 = Axiom().setAttributes([ancv1, ancv2, parv2])
t3ax3 = Axiom().setAttributes([par1])
t3ax4 = Axiom().setAttributes([par2])

th3 = Theorem().setAttributes([Axiom().addPredicate(ancv1)],[t3ax1, t3ax2, t3ax3, t3ax4])

"""
(defvar *premises-4*
  '(((ancestor ?x ?y) (ancestor ?x ?z) (parent ?z ?y))
    ((ancestor ?x ?y) (parent ?x ?y))
    ((parent Mary Paul))
    ((parent Sue Mary))))

(defvar *goals-4*
  '((ancestor ?x ?y)))
"""
th4 = Theorem().setAttributes([Axiom().addPredicate(ancv1)],[t3ax2, t3ax1, t3ax3, t3ax4])

#===========================================================================
#                               THEOREM PROOFS
#===========================================================================
print("=========================PROBLEM 1=========================")
print("=======DFS=======")
th1.prove()                 #DFS
print("\n=======BFS=======")
th1.setSearch(True).prove() #BFS
print()

print("=========================PROBLEM 2=========================")
print("=======DFS=======")
th2.prove()                 #DFS
print("\n=======BFS=======")
th2.setSearch(True).prove() #BFS
print()

print("=========================PROBLEM 3=========================")
print("=======DFS=======")
th3.prove()                 #DFS
print("\n=======BFS=======")
th3.setSearch(True).prove() #BFS
print()

print("=========================PROBLEM 4=========================")
print("=======DFS=======")
th4.prove()                 #DFS
print("\n=======BFS=======")
th1.setSearch(True).prove() #BFS
