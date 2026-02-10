#include <stdio.h>
#include <math.h>

/*
1- Produrre la libreria condivisa "serie" (libserie.so) in cui sia definita la funzione fibonacci che accetti in ingresso il numero intero n;
2- Calcoli i valori della successione di Fibonacci fino al termine Fn e restituisca il valore Fn/Fn-1;
3- Produrre il modulo python (serie.py) che tramite ctypes usi la libreria condivisa libserie.so;
4- Definisca la funzione fibonacci che a sua volta usi quella della libreria c serie;
5- Produrre uno script python (run_serie.py) che importi il modulo fibonacci e usi la corrispondnete funzione fibonacci

Libreria condivisa della serie di Fibonacci che poi viene creata con comando da terminale: 
	gcc -o libserie.so -shared serie.c -O3
*/

double fibonacci(int n){
  
  // Calcola due termini consecutivi della successione di Fibonacci
  if(n>2){
  
    double F_2 = 0.0;
    double F_1 = 1.0;
    double F_n = 0.0;
 
    for(i=3; i<=n; i++){
      F_n = F_2 + F_1;
      F_1 = F_n;
      F_2 = F_1;
    }
    
    // Restituisce il rapporto dei due termini consecutivi calcolati
    double ris = F_1/F_2; 
    
    return ris;
  } 
  
  else{
    
	return 1;
  }
}
