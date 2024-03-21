#include <stdio.h>
#define QTD 256

int main(int argc, char** argv){
	FILE *entrada;
	int c;

	entrada = fopen(argv[1],"rb");
	if(!entrada){
		fprintf(stderr,"Arquivo %s não pode ser aberto para leitura\n", argv[1]);
		return 1;
	}
    
    int ascii[QTD] = {0};
	c = fgetc(entrada);
	while(c != EOF){
        int numero = c;
        ascii[numero]++;
		c = fgetc(entrada);
	}
    for(int i = 0; i < QTD ; i++){
        if(ascii[i] != 0){
            char letra = i;
            // printf("%c\n", letra);
            if(letra == '\n'){
            printf("O programa tem %d quebras de linha\n", ascii[i]);
            }
            else{
            printf("A letra %c apareceu %d vezes no arquivo\n", letra, ascii[i]);
            }
            printf("Posicao na ascii: %d\n", i);
        }
    }
	fclose(entrada);
	return 0;
}