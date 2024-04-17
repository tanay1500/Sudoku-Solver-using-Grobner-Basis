import sympy as sp
from sympy import symbols, groebner, solve
import copy


def red(gb):
    # Minimal Gröbner basis
    temp = copy.deepcopy(gb)
    temp = temp.polys
    G_minimal = []
    while temp:
        f0 = temp.pop()
        if not any(sp.polys.monomials.monomial_divides(f.LM(), f0.LM()) for f in temp + G_minimal):
            G_minimal.append(f0)

    # reduce
    G_reduced = []
    for i, g in enumerate(G_minimal):
        try:
            _, remainder = sp.reduced(g, G_reduced[:i] + G_minimal[i+1:])
            if remainder != 0:
                G_reduced.append(remainder)
        except:
            print("No solutions found")
            return
    
    return G_reduced

def solve_sudoku(sudoku):
    variables = symbols('a1:5 b1:5 c1:5 d1:5')

    equations = []
    #cell constraint
    for var in variables:
        equations.append((var - 1)*(var - 2)*(var - 3)*(var - 4))
    
    #row sum constraint
    for i in range(4):
        equations.append(sum(variables[i * 4 + j] for j in range(4)) - 10)
    
    #column sum constraint
    for j in range(4):
        equations.append(sum(variables[i * 4 + j] for i in range(4)) - 10)

    #row product constraint
    for i in range(4):
        equations.append(variables[i * 4] * variables[i * 4 + 1] * variables[i * 4 + 2] * variables[i * 4 + 3] - 24)
    
    #coulmn product constraint
    for j in range(4):
        equations.append(variables[j] * variables[j + 4] * variables[j + 8] * variables[j + 12] - 24)

    #2x2 sum constraint
    for i in range(4):
        for j in range(4):
            if i % 2 == 0 and j % 2 == 0:
                equations.append(variables[i * 4 + j] + variables[i * 4 + j + 1] + variables[(i + 1) * 4 + j] + variables[(i + 1) * 4 + j + 1] - 10)

    #2x2 product constraint
    for i in range(4):
        for j in range(4):
            if i % 2 == 0 and j % 2 == 0:
                equations.append(variables[i * 4 + j] * variables[i * 4 + j + 1] * variables[(i + 1) * 4 + j] * variables[(i + 1) * 4 + j + 1] - 24)
    
    gb_without_initial_conditions = groebner(equations,variables)
    red_grobner = red(gb_without_initial_conditions)
    print("Reduced Gröbner basis without initial values:")
    for i,g in enumerate(red_grobner):
        print("|||")
        print(i+1)
        print(g)

    #initial conditions
    for i in range(4):
        for j in range(4):
            if sudoku[i][j] != 0:
                equations.append(variables[i * 4 + j] - sudoku[i][j])
    # print(equations)
    # print(len(equations))

    # Compute Gröbner basis
    gb = groebner(equations,variables)
    # print(gb)
    # print(len(gb))

        
    # print(G_reduced)
    try:
        G_reduced = red(gb)
        solutions = []
        #getting solution from G_reduced
        for g in G_reduced:
            solution = solve(g)
            if solution:
                solutions.append(solution)
        
        solutionss = []
        for sol in solutions:
            for sol2 in sol:
                solutionss.append(sol2)

        tempp = []
        temppp = []
        for i in range(0,len(solutionss),4):
            for j in range(4):
                tempp.append(solutionss[i+j])
            #printing reverse of tempp
            temppp.append(tempp[::-1])
            tempp = []
        
        for i in range(len(temppp)-1,-1,-1):
            print(temppp[i])
    except:
        print("Multiple solutions possible")
        return


# Example Sudoku puzzle
sudoku = [
    [0, 0, 3, 1],
    [0, 3, 0, 0],
    [3, 0, 0, 2],
    [2, 0, 4, 0]
]
# sudoku = [
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 0]
# ]

solutions = solve_sudoku(sudoku)