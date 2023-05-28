# Analisador Léxico


### Nesse projeto você vai encontrar 4 arquivos principais:

&nbsp;
- *q1.md* - Definição de tokens e suas respectivas expressões regulares.

- *q2.py* - Apartir de todas as expressões regulares, monta um e-NFA.
    - Esse código gera duas saidas: 
        - Um arquivo CSV (Alfabeto, Estados, Estado Incial, Estados Finais, Identificadores e Transições) para uma visualização mais intuitiva .
        - 6 variáveis que são importadas pela q3. 

- *q3.py* - Apartir do e-NFA da questão anterior, monta um DFA.
    - **Esse processo é um tanto quanto demorado, o arquivo de saida é utilizado na q4, por isso ele já está incluso no projeto.**
    - Esse código gera duas saidas:
        - um arquivo CSV (Alfabeto, Estados, Estado Incial, Estados Finais, Identificadores e Transições) para uma visualização mais intuitiva.
        - Um arquivo .txt que guarda todas as informações do DFA, esse arquivo é utilizado na q4. 

- *q4.py* - Apartir do DFA da questão anterior, monta um analisador léxico.
    - O arquivo entradaQ4.txt contém o código a ser analisado.
    - Esse código gera uma saida:
        - Um arquivo .txt que contém os tokens encontrados no código de entrada.


---

## Arquivos de entrada e saída:


- *saidaQ2.csv* - Arquivo CSV gerado pela q2.py.
- *saidaQ3.csv* - Arquivo CSV gerado pela q3.py.
- *dados.txt* - Arquivo .txt gerado pela q3.py, utilizado pela q4.py.
- *entradaQ4.txt* - Arquivo .txt que contém o código a ser analisado.
- *saidaQ4.txt* - Arquivo .txt gerado pela q4.py que contém os tokens encontrados.


## OBSERVAÇÕES:
- O arquivo solicitado contendo a lista de tokens utilizados e o que eles representam está no arquivo *q1.md*.
- Caso desejado, é possível alterar o código de entrada no arquivo *entradaQ4.txt*.
- No arquivo *saidaQ3.csv* há uma lista com os identificadores dos estados de aceitação
