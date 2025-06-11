#Estudantes
param n; 

#Escolas
param m; 

#Matriz de distâncias do estudante i à escola j
param d {i in 1..n, j in 1..m}; 

#Capacidade de cada escola
param C {j in 1..m};

#Peso para penalidade
param peso;

#Matriz com possíveis penalidades
set Penalizaveis := {i in 1..n, j in 1..m: d[i,j] > 3};

#Variável de decisão, indicando se o estudante i está alocado à escola j
var x {i in 1..n, j in 1..m} binary; 

#Distância máxima que um estudante pode estar alocado
var t;

#Soma
var S;

#Penalidade caso o estudante esteja alocado a uma distância maior que 3km
var penaliza {i in 1..n, j in 1..m} binary;

#Função objetivo com penalidade
minimize maxdist: (S/n) + peso * sum{i in 1..n, j in 1..m} penaliza[i,j];


#Restrições

#Somar a distância somente para a escola alocada
subject to distancia: sum{i in 1..n,j in 1..m} x[i,j]*d[i,j]=S;

#Estudante não pode ser alocado a uma distancia maior que t
subject to distmax {i in 1..n}: sum{j in 1..m} x[i,j]*d[i,j]<=t;

#A distância máxima não pode ser maior que 30
subject to tt: t<=30;

#Cada estudante deve ser alocado a exatamente uma escola
subject to alocaest {i in 1..n}: sum{j in 1..m} x[i,j]=1;

#Cada escola pode receber no máximo a sua capacidade
subject to capacidade {j in 1..m}: sum {i in 1..n} x[i,j]<=C[j];

#Penalidade para alocação de estudantes a escolas a mais de 3km de distância

#Garante que penaliza[i,j] só pode ser 1 se x[i,j] = 1 (ou seja, se o aluno for de fato alocado à escola j)
subject to penalidade1 {i in 1..n, j in 1..m}: penaliza[i,j] <= x[i,j];

#Se o par (i,j) pertence ao conjunto Penalizaveis (distância > 3km), então penaliza[i,j] deve ser 1 quando x[i,j] = 1
subject to penalidade2 {(i,j) in Penalizaveis}: penaliza[i,j] >= x[i,j];

#Se a distância é menor ou igual a 3km, a penalização nunca pode acontecer (independente da alocação)
subject to penalidade3 {(i,j) in (1..n cross 1..m) diff Penalizaveis}: penaliza[i,j] = 0;














