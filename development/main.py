from tkinter import *
from math import *

###########################################################################################
###########################################################################################	
###########################################################################################	
def main(p=50, Itermax=1000):
    import time

    import execute
    import generate
    import get
    import report
    import write

    t0 = time.perf_counter()  # Starts counting time

    profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs = generate.Scenario(p)  # Generate scenario

    t1 = time.perf_counter()  # Records time after scenario generation

    candAval, profSche, sbjBook0, profBook0, profSche0, candOrdered, sbjBook, profBook, profSche = get.InitialSolution(p, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs)  # Get initial solution

    t2 = time.perf_counter()  # Records time after initial solution

    sbjBook, profBook, profSche, sbjBook_best, profBook_best, profSche_best, BestMove_log = execute.TabuSearch(Itermax, sbjHPW, sbjGroups, sbjBook, profBook, profSche, profSubject, profPeriod)  # Runs tabu search algorithm

    t3 = time.perf_counter()  # Records time after tabu search execution

    write.Variables(sbjGroups, profSubject, sbjProfs, candAval, profPeriod, sbjPeriod, sbjHPW, sbjOrdered, sbjBook_best, sbjBook0, profBook_best, profBook0, profSche_best, profSche0, BestMove_log)  # Writes important variables in a file

    print("\nScenario generated in", t1 - t0, "seconds", "\nInitial solution generated in", t2 - t1, "seconds", "\nTabu search run time:", t3 - t2, "seconds")

    report.Classes(sbjBook0, "initial-solution-classes")
    report.Classes(sbjBook_best, "classes")
    report.Schedules(profBook_best, profBook0)

    return


profNumber = input("How many professors there will be in the university? ")
profNumber = int(profNumber)
iterNumber = input(
    "How many iterations do you want Tabu Search algorithm to perform after a solution better than the best so far? ")
iterNumber = int(iterNumber)

main(profNumber, iterNumber)

