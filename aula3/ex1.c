#include <stdio.h>

// stdout, stdin, stderr

int main(int argc, char** argv)
{
	FILE *entrada, *saida;
	int c;

	if(argc != 3)
	{
		fprintf(stderr,"Erro na chamada do comando.\n");
		fprintf(stderr,"Uso: %s [ARQUIVO ORIGEM] [ARQUIVO DESTINO].\n", argv[0]);
		return 1;
	}

	entrada = fopen(argv[1],"rb");
	if(!entrada)
	{
		fprintf(stderr,"Arquivo %s não pode ser aberto para leitura\n", argv[1]);
		return 1;
	}

	saida = fopen(argv[2],"wb");
	if(!saida)
	{
		fclose(entrada);
		fprintf(stderr,"Arquivo %s não pode ser aberto para escrita\n", argv[2]);
		return 1;
	}
	int linhas = 0;
	c = fgetc(entrada);
	while(c != EOF)
	{
		if(c == '\n'){
			linhas++;
		}
		c = fgetc(entrada);
	}

	fclose(entrada);
	fclose(saida);
	printf("%d\n", linhas);
	return 0;
}