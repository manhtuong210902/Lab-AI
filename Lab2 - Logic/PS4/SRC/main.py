import os
import pathlib

## xóa khoảng trắng và xóa dấu xuống dòng trong chuỗi
def removeWhitespace(string: str):
    return string.replace(" ","").replace('\n','')

#đổi dấu 1 literal
def negationOfLiteral(literal:str):
    if len(literal) < 2:
        return "-" + literal
    return literal.replace("-", "")


## Đọc file trả về câu alpha và KB
def readFile(filename : str):
    f = open(filename, "r")
    alpha = removeWhitespace(f.readline()).split('OR')
    KB = []
    nKB = int(f.readline())
    for i in range(nKB):
        i = removeWhitespace(f.readline()).split('OR')
        KB.append(i)

    return alpha, KB

## sắp xếp các literal trong 1 mệnh đề
def sortedLiterals(clause):
    return sorted(clause, key=lambda element: element[-1])

## xóa các literals trùng nhau trong 1 mệnh đề
def removeDuplicateLiterals(clause):
    result = []
    for i in clause:
        if i not in result:
            result.append(i)
    return result

##dạng chuẩn của một mệnh đề
def standardForm(clause):
    result = removeDuplicateLiterals(clause)
    return sortedLiterals(result)



def isSublistOf(l1, l2):
    for element in l1:
        if not element in l2:
            return False
    return True

## kiểm tra một mệnh đề có hợp lệ
## A OR B OR -B không hợp lệ: False
def orContainTautology(clause):
    for item in clause:
        if negationOfLiteral(item) in clause:
            return True
    return False

def reFormatClause(clause):
    if len(clause) == 0:
        return "{}"
    
    formatedClause = ""
    for i in range(len(clause) - 1):
        formatedClause += clause[i] + " OR "
    formatedClause += clause[-1]

    return formatedClause

def plResovle(clause_i, clause_j):
    clauses = []
    for l_i in clause_i:
        for l_j in clause_j:
            if negationOfLiteral(l_i) == l_j or negationOfLiteral(l_j) == l_i:
                clause_i_re = [n for n in clause_i if n != l_i]
                clause_j_re = [n for n in clause_j if n != l_j]
                clauses.append(standardForm(clause_i_re + clause_j_re))         
    return clauses

def plResolution(alpha, KB):
    #clauses = KB
    clauses = list(map(standardForm, KB))
    
    #phủ định lại câu alpha đưa vào KB
    for literal in alpha:
        #phủ định câu alpha
        clause = [negationOfLiteral(literal)]
        #thêm vào danh sách mệnh đề
        clauses.append(clause)

    #khỏi tạo ds mới bằng mảng rỗng
    newList = []

    rs = []
    solution = False
    i = 0
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        rs.append([])
        for (clause_i, clause_j) in pairs:
            #chạy vòng lặp xét 2 cặp mệnh đề trong clause
            resolvents = plResovle(clause_i, clause_j)
            if [] in resolvents:
                solution = True
            for tempCR in resolvents:
                if orContainTautology(tempCR):
                    break
                if not tempCR in newList:
                    newList.append(tempCR)   
                    if tempCR not in clauses:
                        rs[-1].append(tempCR)
        i += 1           

        if solution == True:
            return solution, rs

        if isSublistOf(newList, clauses):
            solution = False
            return solution, rs
 
        for c in newList:
            if not c in clauses:
                clauses.append(c)

def writeFile(filename, solution:bool, result:list):
    f = open(filename, "w") 
    for clauses in result:
        f.write(str(len(clauses)) + '\n')
        for clause in clauses:
            f.write(reFormatClause(clause) + '\n')

    if solution == True:
        f.write('YES' + '\n')
    else:
        f.write('NO' + '\n')

    f.close()


def main():
    dir = pathlib.Path().resolve()
    inputList = os.listdir(os.path.join(dir,"INPUT"))

    for i in range(len(inputList)):
        inputList[i] = os.path.join(dir, 'INPUT','input' + str(i) +'.txt')

    outputList = []

    for i in range(len(inputList)):
        outputList.append(os.path.join(dir,"OUTPUT",'output' +str(i)+'.txt'))


    for i in range(len(inputList)):
        alpha, KB = readFile(inputList[i])
        solution, rs = plResolution(alpha, KB)
        writeFile(outputList[i], solution, rs)

if __name__ == '__main__':
    main()





