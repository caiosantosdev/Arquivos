#include <stdio.h>
#include <string.h>

typedef struct _Endereco Endereco;

struct _Endereco
{
	char logradouro[72];
	char bairro[72];
	char cidade[72];
	char uf[72];
	char sigla[2];
	char cep[8];
	char lixo[2];
};

int main(int argc, char**argv)
{
	FILE *f;
	Endereco e;
	long archiveSize, inicio, meio, fim;
    int loopCounter = 0;
    int finded = 0;
    

	if(argc != 3)
	{
		fprintf(stderr, "USO: %s ENDERECO_ARQUIVO [CEP]", argv[0]);
		return 1;
	}

	printf("Tamanho da Estrutura: %ld\n\n", sizeof(Endereco));
	f = fopen(argv[1],"rb");
    if(f){
        printf("Arquivo aberto\n");
    }
    fseek(f,0,SEEK_END);
    archiveSize = ftell(f);
    fseek(f,0,SEEK_SET);
    inicio = 0;
    fim = (archiveSize / sizeof(Endereco)) - 1;

	while(inicio <= fim)
	{
        meio = (inicio + fim) / 2;
		loopCounter++;
        fseek(f, meio * sizeof(Endereco), SEEK_SET);
        fread(&e, sizeof(Endereco),1,f);

		if(strncmp(argv[2],e.cep,8)==0)
		{
            printf("Endereço encontrado! \n");
			printf("%.72s\n%.72s\n%.72s\n%.72s\n%.2s\n%.8s\n",e.logradouro,e.bairro,e.cidade,e.uf,e.sigla,e.cep);
			finded = 1;
            break;
		}
        else if(strncmp(argv[2],e.cep,8)>0){
            inicio = meio + 1;
        }
        else if(strncmp(argv[2],e.cep,8)<0){
            fim = meio - 1;
        }	
	}
    if(!finded){
        printf("Endereco nao encontrado\n");
    }
	printf("Total de leituras: %d\n", loopCounter);
	fclose(f);
}
