#DEFINIÇÃO DOS TOKENS
OPERATOR_ADD = "(+)"
OPERATOR_SUB = "(_)"
OPERATOR_MUL = "(:)"
OPERATOR_DIV = "(/)"
OPERATOR_ASSIGN = "(=)"
PUNCTUATION_SEMICOLON = "(;)"
PUNCTUATION_COMMA = "(,)"
PARENTHESIS_LEFT = "(°)"
PARENTHESIS_RIGHT = "(^)"
BRACE_LEFT = "({)"
BRACE_RIGHT = "(})"
IF = "(i.f)"
ELSE = "(e.(l.(s.e)))"
KEYWORD_INT = "(i.(n.t))"
RETURN = "(r.(e.(t.(u.(r.n)))))"
KEYWORD_STRING = "(s.(t.(r.(i.(n.g)))))"
INT = "((0|(1|(2|(3|(4|(5|(6|(7|(8|9))))))))).((0|(1|(2|(3|(4|(5|(6|(7|(8|9)))))))))*))"
STRING = '(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((a|b)|c)|d)|e)|f)|g)|h)|i)|j)|k)|l)|m)|n)|o)|p)|q)|r)|s)|t)|u)|v)|w)|x)|y)|z)|A)|B)|C)|D)|E)|F)|G)|H)|I)|J)|K)|L)|M)|N)|O)|P)|Q)|R)|S)|T)|U)|V)|W)|X)|Y)|Z)|0)|1)|2)|3)|4)|5)|6)|7)|8)|9)|").(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((a|b)|c)|d)|e)|f)|g)|h)|i)|j)|k)|l)|m)|n)|o)|p)|q)|r)|s)|t)|u)|v)|w)|x)|y)|z)|A)|B)|C)|D)|E)|F)|G)|H)|I)|J)|K)|L)|M)|N)|O)|P)|Q)|R)|S)|T)|U)|V)|W)|X)|Y)|Z)|0)|1)|2)|3)|4)|5)|6)|7)|8)|9)|")*))'
IDENTIFIER = "((((((((((((((((((((((((((((((((((((((((((((((((((((a|b)|c)|d)|e)|f)|g)|h)|i)|j)|k)|l)|m)|n)|o)|p)|q)|r)|s)|t)|u)|v)|w)|x)|y)|z)|A)|B)|C)|D)|E)|F)|G)|H)|I)|J)|K)|L)|M)|N)|O)|P)|Q)|R)|S)|T)|U)|V)|W)|X)|Y)|Z).((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((a|b)|c)|d)|e)|f)|g)|h)|i)|j)|k)|l)|m)|n)|o)|p)|q)|r)|s)|t)|u)|v)|w)|x)|y)|z)|A)|B)|C)|D)|E)|F)|G)|H)|I)|J)|K)|L)|M)|N)|O)|P)|Q)|R)|S)|T)|U)|V)|W)|X)|Y)|Z)|0)|1)|2)|3)|4)|5)|6)|7)|8)|9)*))"

class NFA:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        self.states.append(state)

    def add_symbol(self, symbol):
        self.alphabet.append(symbol)
    def add_transition(self, state, symbol, next_states):
        if (state, symbol) not in self.transitions:
            self.transitions[(state, symbol)] = set()
        self.transitions[(state, symbol)].update(next_states)

    def set_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        self.final_states.add(state)


#IMPRIME AS TRNASIÇÕES DE UMA FORMA MAIS LEGÍVEL, USADA PARA DEBUG 
def imprimir_transicoes(nfa):
    for transition in nfa.transitions.items():
        for elemento in transition[1]:
            print(transition[0][0], "(", transition[0][1],") ->", elemento)


# O NFA É UMA QUINTUPLA (S,Σ,δ,s0,F), ONDE CADA ELEMENTO É:
# S Conjunto finito de estados
# Σ Conjunto finito de símbolos de entrada (alfabeto)
# δ Conjunto de transições
# s0 Estado inicial
# F Conjunto de estados finais
# Tendo isso em vista o código abaixo coloca o codigo em csv de forma legível para humanos 

def transitions_to_CSV(nfa, identificadores):
    file = open("saidaQ2.csv", "w")

    alphabet = "Alfabeto;"
    for symbol in nfa.alphabet:
        if (symbol == nfa.alphabet[-1]):
            alphabet += symbol
        else:
            alphabet += symbol + ","
    file.write(alphabet)
    file.write("\n")

    states = ""
    for symbol in nfa.states:
        if (symbol == nfa.states[-1]):
            states += "q"+str(symbol)
        else:
            states += "q"+str(symbol)+","
    states = "S;"+states
    file.write(states)
    file.write("\n")

    file.write("S0;"+ "q"+str(nfa.start_state))
    file.write("\n")


    #passa o conjunto de estados finais para uma string separada por virgula, como é um set não posso iterar 
    #diretamente, por isso passo para uma lista e depois para uma string

    final = ""    
    lista_final = list(nfa.final_states)
    for symbol in lista_final:
        if (symbol == lista_final[-1]):
            final += "q"+str(symbol)
        else:
            final += "q"+str(symbol)+","

    final_states = "F;"+final
    file.write(final_states)
    file.write("\n")

    file.write("\n")
    file.write("IDENTIFICADORES:")
    file.write("\n")
    for estado in identificadores:
        id_str = "q"+str(estado[0]) + ";" + estado[1]        
        file.write(id_str)
        file.write("\n")
    file.write("\n")
    file.write("\n")

    for transition in nfa.transitions.items():
        for elemento in transition[1]:
            symbol = transition[0][1]
            if (symbol == ""):
                symbol = "-"
            stringCompleta = ("q"+str(transition[0][0]) + ";" + symbol +";"+ "q"+str(elemento))
            file.write(stringCompleta)
            file.write("\n")
    file.close()


#FUNÇÕES A SEREM CHAMADAS NO ALGORÍTIMO DE THOMPSON
def concatenacao(nfa1, nfa2):
    nfa = NFA()
    nfa.add_state(1)
    nfa.set_start_state(1)
    nfa.add_transition(1,'',{2})
    tamanho_adicionar = len(nfa1.states)+1

    for transition in nfa1.transitions.items():
        for destino in transition[1]:
            nfa.add_transition(transition[0][0]+1, transition[0][1],{destino+1} )

    for state in nfa1.states:
        nfa.add_state(state+1)

    nfa.add_transition(tamanho_adicionar,'',{tamanho_adicionar+1})

    for transition in nfa2.transitions.items():
        for destino in transition[1]:
            nfa.add_transition(transition[0][0]+tamanho_adicionar, transition[0][1],{destino+tamanho_adicionar} )
        
    for state in nfa2.states:
        nfa.add_state(state+tamanho_adicionar)

    nfa.add_final_state(len(nfa1.states)+len(nfa2.states)+1)
    return nfa

def or_case(nfa1, nfa2):
    nfa = NFA()
    nfa.add_state(1)
    nfa.add_state(2)
    nfa.add_state(3)
    nfa.set_start_state(1)
    nfa.add_transition(1,'',{2})
    nfa.add_transition(1,'',{3})
    
    tamanho_adicionar = len(nfa1.states)+3    

    nfa.add_transition(2,'',{4})
    nfa.add_transition(3,'',{tamanho_adicionar+1})

    nfa1_att = NFA()
    for transition in nfa1.transitions.items():
        for destino in transition[1]:
            nfa1_att.add_transition(transition[0][0]+3, transition[0][1],{destino+3} )

    for state in nfa1.states:
        nfa.add_state(state+3)

    nfa2_att = NFA()
    for transition in nfa2.transitions.items():
        for destino in transition[1]:
            nfa2_att.add_transition(transition[0][0]+tamanho_adicionar, transition[0][1],{destino+tamanho_adicionar} )    
    
    for state in nfa2.states:
        nfa.add_state(state+tamanho_adicionar)


    for transition in nfa1_att.transitions.items():
            for destino in transition[1]:
                nfa.add_transition(transition[0][0], transition[0][1],{destino} )    

    for transition in nfa2_att.transitions.items():
            for destino in transition[1]:
                nfa.add_transition(transition[0][0], transition[0][1],{destino} )    

    estado_final = len(nfa1.states)+len(nfa2.states)+3+1
    nfa.add_state(estado_final)
    nfa.add_final_state(estado_final)
    nfa.add_transition((len(nfa1.states)+3),'',{estado_final})
    nfa.add_transition((len(nfa1.states)+len(nfa2.states)+3),'',{estado_final})
    return nfa
    
def kleene(nfa1):
    nfa = NFA()
    nfa.add_state(1)
    nfa.set_start_state(1)
    nfa.add_transition(1,'',{2})
    nfa.add_state(len(nfa1.states)+2)
    nfa.add_final_state(len(nfa1.states)+2)
    nfa.add_transition(1,'',{len(nfa1.states)+2})

    for state in nfa1.states:
        nfa.add_state(state+1)

    for transition in nfa1.transitions.items():
        for destino in transition[1]:
            nfa.add_transition(transition[0][0]+1, transition[0][1],{destino+1} )

    nfa.add_transition(len(nfa1.states)+1,'',{len(nfa1.states)+2})
    nfa.add_transition(len(nfa1.states)+1,'',{2})
    return nfa


#ALGORITMO DE THOMPSON
def converter_ER_to_NFA_aux(pilha):
    nfa = NFA()
    simboloAnterior = 0
    while True:
        simbolo = pilha.pop()
        if simbolo == '.':
            nfa1 = simboloAnterior
            nfa2 = pilha.pop()
            nfa = concatenacao(nfa2, nfa1)
        if simbolo =='|':
            nfa1 = simboloAnterior
            nfa2 = pilha.pop()
            nfa = or_case(nfa1, nfa2)
        if simbolo == '*':
            nfa1 = pilha.pop()
            nfa = kleene(nfa1)

        simboloAnterior = simbolo
        if (simbolo == '('): break
    return nfa, pilha


def preparar_lista(ER):
    lista_ER = []
    for symbol in ER:
        if  symbol == '*' or symbol == '(' or symbol == ')' or symbol == '|' or symbol == '.':
            lista_ER.append(symbol)
        else:
            nfa = NFA()
            startState = 1
            finalState = 2
            nfa.add_state(startState)
            nfa.add_state(finalState)
            nfa.set_start_state(startState)
            nfa.add_final_state(finalState)
            nfa.add_transition(startState, symbol, {finalState})
            lista_ER.append(nfa)
    return lista_ER


def converter_ER_to_NFA(ER):
    pilha = []
    lista_ER = (preparar_lista(ER))
    for i in range(len(lista_ER)):
        if(lista_ER[i] != ')'):
            pilha.append(lista_ER[i])
        if(lista_ER[i] == ')'):
            if(len(pilha) == 2):
                return (pilha[1])

            else:
                NFA, pilha = converter_ER_to_NFA_aux(pilha) 
                pilha.append(NFA)
    return NFA


#CRIA 1 NFA PARA CADA TOKEN

nfa_OPERATOR_ADD = NFA()
nfa_OPERATOR_ADD.alphabet = ['+']
nfa_OPERATOR_ADD = converter_ER_to_NFA(OPERATOR_ADD)

nfa_OPERATOR_SUB = NFA()
nfa_OPERATOR_SUB.alphabet = ['_']
nfa_OPERATOR_SUB = converter_ER_to_NFA(OPERATOR_SUB)

nfa_OPERATOR_MUL = NFA()
nfa_OPERATOR_MUL.alphabet = [':']
nfa_OPERATOR_MUL = converter_ER_to_NFA(OPERATOR_MUL)

nfa_OPERATOR_DIV = NFA()
nfa_OPERATOR_DIV.alphabet = ['/']
nfa_OPERATOR_DIV = converter_ER_to_NFA(OPERATOR_DIV)

nfa_OPERATOR_ASSIGN = NFA()
nfa_OPERATOR_ASSIGN.alphabet = ['=']
nfa_OPERATOR_ASSIGN = converter_ER_to_NFA(OPERATOR_ASSIGN)

nfa_PUNCTUATION_SEMICOLON = NFA()
nfa_PUNCTUATION_SEMICOLON.alphabet = [';']
nfa_PUNCTUATION_SEMICOLON = converter_ER_to_NFA(PUNCTUATION_SEMICOLON)

nfa_PUNCTUATION_COMMA = NFA()
nfa_PUNCTUATION_COMMA.alphabet = [',']
nfa_PUNCTUATION_COMMA = converter_ER_to_NFA(PUNCTUATION_COMMA)

nfa_PARENTHESIS_LEFT = NFA()
nfa_PARENTHESIS_LEFT.alphabet = ['°']
nfa_PARENTHESIS_LEFT = converter_ER_to_NFA(PARENTHESIS_LEFT)

nfa_PARENTHESIS_RIGHT = NFA()
nfa_PARENTHESIS_RIGHT.alphabet = ['^']
nfa_PARENTHESIS_RIGHT = converter_ER_to_NFA(PARENTHESIS_RIGHT)

nfa_BRACE_LEFT = NFA()
nfa_BRACE_LEFT.alphabet = ['{']
nfa_BRACE_LEFT = converter_ER_to_NFA(BRACE_LEFT)

nfa_BRACE_RIGHT = NFA()
nfa_BRACE_RIGHT.alphabet = ['}']
nfa_BRACE_RIGHT = converter_ER_to_NFA(BRACE_RIGHT)

nfa_IF = NFA()
nfa_IF.alphabet = ['i','f']
nfa_IF = converter_ER_to_NFA(IF)

nfa_ELSE = NFA()
nfa_ELSE.alphabet = ['e','l','s']
nfa_ELSE = converter_ER_to_NFA(ELSE)

nfa_KEYWORD_INT = NFA()
nfa_KEYWORD_INT.alphabet = ['i','n','t']
nfa_KEYWORD_INT = converter_ER_to_NFA(KEYWORD_INT)

nfa_RETURN = NFA()
nfa_RETURN.alphabet = ['r','e','t','u','r','n']
nfa_RETURN = converter_ER_to_NFA(RETURN)

nfa_KEYWORD_STRING = NFA()
nfa_KEYWORD_STRING.alphabet = ['s','t','r','i','n','g']
nfa_KEYWORD_STRING = converter_ER_to_NFA(KEYWORD_STRING)

nfa_INT = NFA() 
nfa_INT.alphabet = ['0','1','2','3','4','5','6','7','8','9']
nfa_INT = converter_ER_to_NFA(INT)

nfa_STRING = NFA()
nfa_STRING.alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                           'q','r','s','t','u','v','x','w','y','z','A','B','C','D','E','F',
                           'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
                           'X','W','Y','Z','0','1','2','3','4','5','6','7','8','9']
nfa_STRING = converter_ER_to_NFA(STRING)


nfa_IDENTIFIER = NFA()
nfa_IDENTIFIER.alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                           'q','r','s','t','u','v','x','w','y','z','A','B','C','D','E','F',
                           'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
                           'X','W','Y','Z','0','1','2','3','4','5','6','7','8','9']
nfa_IDENTIFIER = converter_ER_to_NFA(IDENTIFIER)


#Cria um NFA, cria um estado inicial e liga ao estado inicial de todos os outros NFAs
nfa = NFA()

nfa.add_state(1)
nfa.set_start_state(1)
adicionar = 1
identificadores = []
nfa.alphabet = []

#Adiciona os estados e transições do todos os NFAs para o NFA principal

nfa.add_transition(1, '', {2})
for transition in nfa_OPERATOR_ADD.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)

for state in nfa_OPERATOR_ADD.states:
    nfa.add_state(state+adicionar)
for final in nfa_OPERATOR_ADD.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"OPERATOR_ADD"))

adicionar = adicionar + len(nfa_OPERATOR_ADD.states)
nfa.alphabet.append('+')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_OPERATOR_SUB.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_OPERATOR_SUB.states:
    nfa.add_state(state+adicionar)
for final in nfa_OPERATOR_SUB.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"OPERATOR_SUB"))

adicionar = adicionar + len(nfa_OPERATOR_SUB.states)
nfa.alphabet.append('_')


destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_OPERATOR_MUL.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_OPERATOR_MUL.states:
    nfa.add_state(state+adicionar)
for final in nfa_OPERATOR_MUL.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"OPERATOR_MUL"))

adicionar = adicionar + len(nfa_OPERATOR_MUL.states)
nfa.alphabet.append(':')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_OPERATOR_DIV.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_OPERATOR_DIV.states:
    nfa.add_state(state+adicionar)
for final in nfa_OPERATOR_DIV.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"OPERATOR_DIV"))

adicionar = adicionar + len(nfa_OPERATOR_DIV.states)
nfa.alphabet.append('/')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_OPERATOR_ASSIGN.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_OPERATOR_ASSIGN.states:
    nfa.add_state(state+adicionar)
for final in nfa_OPERATOR_ASSIGN.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"OPERATOR_ASSIGN"))

adicionar = adicionar + len(nfa_OPERATOR_ASSIGN.states)
nfa.alphabet.append('=')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_PUNCTUATION_SEMICOLON.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_PUNCTUATION_SEMICOLON.states:
    nfa.add_state(state+adicionar)
for final in nfa_PUNCTUATION_SEMICOLON.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"PUNCTUATION_SEMICOLON"))

adicionar = adicionar + len(nfa_PUNCTUATION_SEMICOLON.states)
nfa.alphabet.append(';')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_PUNCTUATION_COMMA.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_PUNCTUATION_COMMA.states:
    nfa.add_state(state+adicionar)
for final in nfa_PUNCTUATION_COMMA.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"PUNCTUATION_COMMA"))

adicionar = adicionar + len(nfa_PUNCTUATION_COMMA.states)
nfa.alphabet.append(',')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_PARENTHESIS_LEFT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_PARENTHESIS_LEFT.states:
    nfa.add_state(state+adicionar)
for final in nfa_PARENTHESIS_LEFT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"PARENTHESIS_LEFT"))

adicionar = adicionar + len(nfa_PARENTHESIS_LEFT.states)
nfa.alphabet.append('°')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_PARENTHESIS_RIGHT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_PARENTHESIS_RIGHT.states:
    nfa.add_state(state+adicionar)
for final in nfa_PARENTHESIS_RIGHT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"PARENTHESIS_RIGHT"))

adicionar = adicionar + len(nfa_PARENTHESIS_RIGHT.states)
nfa.alphabet.append('^')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_BRACE_LEFT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_BRACE_LEFT.states:
    nfa.add_state(state+adicionar)
for final in nfa_BRACE_LEFT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"BRACE_LEFT"))

adicionar = adicionar + len(nfa_BRACE_LEFT.states)
nfa.alphabet.append('{')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_BRACE_RIGHT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_BRACE_RIGHT.states:
    nfa.add_state(state+adicionar)
for final in nfa_BRACE_RIGHT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"BRACE_RIGHT"))

adicionar = adicionar + len(nfa_BRACE_RIGHT.states)
nfa.alphabet.append('}')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_IF.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_IF.states:
    nfa.add_state(state+adicionar)
for final in nfa_IF.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"IF"))

adicionar = adicionar + len(nfa_IF.states)
nfa.alphabet.extend(['i','f'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_ELSE.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_ELSE.states:
    nfa.add_state(state+adicionar)
for final in nfa_ELSE.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"ELSE"))

adicionar = adicionar + len(nfa_ELSE.states)
nfa.alphabet.extend(['e','l','s'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_KEYWORD_INT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_KEYWORD_INT.states:
    nfa.add_state(state+adicionar)
for final in nfa_KEYWORD_INT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"KEYWORD_INT"))

adicionar = adicionar + len(nfa_KEYWORD_INT.states)
nfa.alphabet.extend(['n','t'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_RETURN.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_RETURN.states:
    nfa.add_state(state+adicionar)
for final in nfa_RETURN.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"RETURN"))

adicionar = adicionar + len(nfa_RETURN.states)
nfa.alphabet.extend(['r','u'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_KEYWORD_STRING.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_KEYWORD_STRING.states:
    nfa.add_state(state+adicionar)
for final in nfa_KEYWORD_STRING.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"KEYWORD_STRING"))


adicionar = adicionar + len(nfa_KEYWORD_STRING.states)
nfa.alphabet.append('g')

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_INT.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_INT.states:
    nfa.add_state(state+adicionar)
for final in nfa_INT.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"INT"))

adicionar = adicionar + len(nfa_INT.states)
nfa.alphabet.extend(['0','1','2','3','4','5','6','7','8','9'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_STRING.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_STRING.states:
    nfa.add_state(state+adicionar)
for final in nfa_STRING.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"STRING"))

adicionar = adicionar + len(nfa_STRING.states)
nfa.alphabet.extend(['a','b','c','d','h','j','k','m','o','p',
                           'q','v','x','w','y','z','A','B','C','D','E','F',
                           'G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
                           'X','W','Y','Z','"'])

destino = set()
destino.add(len(nfa.states)+1)
nfa.add_transition(1, '', destino)
for transition in nfa_IDENTIFIER.transitions.items():
    origem = transition[0][0]+adicionar
    simbolo = transition[0][1]
    destino = set()
    for destination in transition[1]:
        destino.add(destination+adicionar)
    nfa.add_transition(origem, simbolo, destino)
for state in nfa_IDENTIFIER.states:
    nfa.add_state(state+adicionar)
for final in nfa_IDENTIFIER.final_states:
    nfa.add_final_state(final+adicionar)
    identificadores.append((final+adicionar,"IDENTIFIER"))


# print(nfa.states)
# print(nfa.transitions)
# print(nfa.final_states)
# print(identificadores)


transitions_to_CSV(nfa, identificadores)

#Variaveis para serem importadas pela Q3
exportTransitions = nfa.transitions
exportAlphabet = nfa.alphabet
exportStates = nfa.states
exportFinalStates = nfa.final_states
exportStartState = nfa.start_state
exportIdentificadores = identificadores
