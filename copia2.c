#include <stdio.h>

#define TAMANHO 4096

int main(int argc, char** argv){
    FILE *entrada, *saida;
    char buffer[TAMANHO];
    int qtd;
    
    if(argc != 3){
        fprintf(stderr, "Erro na cahamada do comando.\n");
        fprintf(stderr, "Uso %s [ARQUIVO ORIGEM] ARQUIVO DESTINO. \n");
        return 1;
    }
    
    
    
}