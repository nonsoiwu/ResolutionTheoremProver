from theorem_prover import *

#====================================================
#                        SET UP
#====================================================

#=============Test Variables=============
pv1 = pElement().setAttributes("x", "?")
pv2 = pElement().setAttributes("y", "?")
pv3 = pElement().setAttributes("z", "?")
pv4 = pElement().setAttributes("w", "?")
pv4n = pElement().setAttributes("w", "?").negate()

#=============Test Zero=============
#Only one is needed since zeroes behave the same
pz = pElement().setAttributes("zo", "z")

#=============Test Constants=============
pc1 = pElement().setAttributes("3", "c")
pc2 = pElement().setAttributes("2", "c")
pc3 = pElement().setAttributes("7", "c")

#=============Test Predicates=============
#1. (x, 3, x)
pr1 = Predicate().setAttributes("test",[pv1, pc1, pv1])

#2. (2, 3, 2)
pr2 = Predicate().setAttributes("test",[pc2, pc1, pc2])

#3. (2, y, 2)
pr3 = Predicate().setAttributes("test",[pc2, pv2, pc2])

#4. (z, y, 2)
pr4 = Predicate().setAttributes("test",[pv3, pv2, pc2])

#5. (x, 3, y)
pr5 = Predicate().setAttributes("test",[pv1, pc1, pv2])

#8. (2, z, w)
pr6 = Predicate().setAttributes("test",[pc2, pv3, pv4])

#More Predicate Test Cases
#1. (x, x, 7)
tpr1 = Predicate().setAttributes("test2",[pv1, pv1, pv3])

#2. (z, y, 2)
tpr2 = Predicate().setAttributes("test2",[pv3, pv2, pc2])

#3. (~w)
tpr3 = Predicate().setAttributes("test3",[pv4n])

#=============Test Axioms=============
#1. ((x, 3, x))
ax1 = Axiom().addPredicate(pr1)

#2. ((2, 3, 2), ~(2, y, 2))
ax2 = Axiom().addPredicate(pr2).addPredicate(pr4)

#3. ((2, y, 2))
ax3 = Axiom().addPredicate(pr3)

ax4 = Axiom().addPredicate(tpr3)

#=============Test Bind Dictionary=============
#Added x -> y
#Added x -> 3
bd1 = bindDict().add(pv1, pv2).add(pv1, pc1)

#Added x -> y
#Added x -> z
#Added x -> w
bd2 = bindDict().add(pv1, pv2).add(pv1, pv3).add(pv1, pv4)

#Added x -> y
#Added z -> w
#Added x -> w
bd3 = bindDict().add(pv1, pv2).add(pv3, pv4).add(pv1, pv4)

#==============Example Assets=====================
#Graph example:

ePV1 = pElement().setAttributes("x","?")      #?x
ePV2 = pElement().setAttributes("y","?")      #?y
ePV3 = pElement().setAttributes("z","?")      #?z

ePC1 = pElement().setAttributes("Brian", "c") #Brian
ePC2 = pElement().setAttributes("Doug", "c")  #Doug
ePC3 = pElement().setAttributes("Mary", "c")  #Mary
ePC4 = pElement().setAttributes("Sue", "c")   #Sue

ePr1 = Predicate().setAttributes("grandparent",[ePV1, ePV2])
ePr2 = Predicate().setAttributes("parent",[ePV1, ePV3])
ePr3 = Predicate().setAttributes("parent",[ePV3, ePV2])
ePr4 = Predicate().setAttributes("parent",[ePC1, ePC2])
ePr5 = Predicate().setAttributes("parent",[ePC2, ePC3])
ePr6 = Predicate().setAttributes("parent",[ePC3, ePC4])
ePr7 = Predicate().setAttributes("grandparent",[ePV3, ePC4])

eAx1 = Axiom().setAttributes([ePr1, ePr2, ePr3])
eAx2 = Axiom().setAttributes([ePr4])
eAx3 = Axiom().setAttributes([ePr5])
eAx4 = Axiom().setAttributes([ePr6])
eAx5 = Axiom().setAttributes([ePr1])
eAx6 = Axiom().setAttributes([ePr7])

eTh = Theorem().setAttributes([eAx5],[eAx1,eAx2,eAx3,eAx4])
eTh2 = Theorem().setAttributes([eAx6],[eAx1,eAx2,eAx3,eAx4])
#====================================================
#                   UNIFICATION TESTS
#====================================================

print("====================================================")
print("                   UNIFICATION TESTS")
print("====================================================")
tbD = bindDict()

un1 = unify(pr1, pr1, bindDict())
#Expected: []
#Reason: Both pr1 and pr1 are identical
print("unify(pr1, pr1, bindDict())")
print("pr1:", pr1.toString())
print("pr1:", pr1.toString())
print("Expected: \n[]")
print("Actual: ")
readBindings(un1)

print()
print("unify(pr1, pr2, bindDict())")
print("pr1:", pr1.toString())
print("pr2:", pr2.toString())
print("Expected: \nx -> 2")
un2 = unify(pr1, pr2, bindDict())
print("Actual: ")
readBindings(un2)

print()
un3 = unify(pr1, pr3, bindDict())
print("unify(pr1, pr3, bindDict())")
print("pr1:", pr1.toString())
print("pr3:", pr3.toString())
print("Expected: \nx -> 2\ny -> 3")
print("Actual: ")
readBindings(un3)

print()
un4 = unify(pr1, pr4, bindDict())
print("unify(pr1, pr4, bindDict())")
print("pr1:", pr1.toString())
print("pr4:", pr4.toString())
print("Expected: \nx -> z\nx -> 2\ny -> 3")
print("Actual: ")
readBindings(un4)
chasify(Axiom().addPredicate(pr1), un4)

print()
un5 = unify(pr5, pr4, bindDict())
print("unify(pr5, pr4, bindDict())")
print("pr5:", pr5.toString())
print("pr4:", pr4.toString())
print("Expected: \nx -> z\ny -> 3\ny -> 2")
print("Actual: ")
readBindings(un5)

print()
un8 = unify(pr5, pr6, bindDict())
print("unify(pr5, pr6, bindDict())")
print("pr5:", pr5.toString())
print("pr6:", pr6.toString())
print("Expected: \nx -> 2\nz -> 3\ny -> w")
print("Actual: ")
readBindings(un8)

print()
unt = unify(tpr1, tpr2, bindDict())
print("unify(tpr5, tpr2, bindDict())")
print("tpr1:", tpr1.toString())
print("tpr2:", tpr2.toString())
print("Expected: \nx -> z\nx -> y\nz -> 2")
print("Actual: ")
readBindings(unt)

#====================================================
#                   BINDING TESTS
#====================================================

print()
print("====================================================")
print("                   BINDING TESTS")
print("====================================================")
print()

bd1.add(pv1, pv2).add(pv1, pc1)
print("bd1.add(pv1, pv2).add(pv1, pc1)")
print("Added:\nx -> y\nx -> 3")
print("Result:")
bd1.show()
print("Showing binds for 'x':")
binds = binding(pv1, bd1)
bstr = ""
for b in binds:
    bstr += b.toString() + " "
print(bstr)

print()
bd2.add(pv1, pv2).add(pv1, pv3).add(pv1, pv4)
print("bd2.add(pv1, pv2).add(pv1, pv3).add(pv1, pv4)")
print("Added:\nx -> y\nx -> z\nx -> w")
print("Result:")
bd2.show()
print("Showing binds for 'x':")
binds = binding(pv1, bd2)
bstr = ""
for b in binds:
    bstr += b.toString() + " "
print(bstr)

print()
bd3.add(pv1, pv2).add(pv3, pv4).add(pv1, pv4).add(pv4, pc1)
print("bd3.add(pv1, pv2).add(pv3, pv4).add(pv1, pv4).add(pv4, pc1)")
print("Added:\nx -> y\nz -> w\nx -> w\nw -> 3")
print("Result:")
bd3.show()
print("Showing binds for 'x':")
binds = binding(pv1, bd3)
bstr = ""
for b in binds:
    bstr += b.toString() + " "
print(bstr)

#====================================================
#                   UNIQUIFY TESTS
#====================================================
print()
print("====================================================")
print("                   UNIQUIFY TESTS")
print("====================================================")
print()
uax1 = uniquify(ax1, bindDict())
print("uniquify(ax1, bindDict())")
print("ax1: " + ax1.toString())
print("uax1: " + uax1.toString())

print()
print(ax2.toString())
uax2 = uniquify(ax2, bindDict())
print("uniquify(ax2, bindDict())")
print("ax2: " + ax2.toString())
print("uax2: " + uax2.toString())

print()
uax3 = uniquify(ax4, bindDict())
print("uniquify(ax4, bindDict())")
print("ax4: " + ax4.toString())
print("uax3: " + uax3.toString())

#====================================================
#                   THEOREM TESTS
#====================================================
print()
print("====================================================")
print("                   THEOREM TESTS")
print("====================================================")
print()

eTh.prove()                  #DFS
print()
eTh.setSearch(True).prove()  #BFS
print()

eTh2.prove()                 #DFS
print()
eTh2.setSearch(True).prove() #BFS
