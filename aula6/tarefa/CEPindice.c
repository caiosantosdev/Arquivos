#include <stdio.h>
#include <string.h>
#include<stdlib.h>

typedef struct _Endereco Endereco;
typedef struct _CEP CEP;
// registroCEP = struct.Struct("72s72s72s72s2s8s2s")

struct _Endereco
{
	char logradouro[72];
	char bairro[72];
	char cidade[72];
	char uf[72];
	char sigla[2];
	char cep[8];
	char lixo[2]; // Ao Espaço no final da linha + quebra de linha
};

struct _CEP{
    char cep[8];
    int indice;  
};

int compara(const void *e1, const void *e2)
{
	return strncmp(((CEP*)e1)->cep,((CEP*)e2)->cep,8);
}

int main(int argc, char**argv)
{
    //file pointer para o arquivo de entrada
	FILE *cepNormal;
    //file pointer para o arquivo de saida
    FILE *escrita;
	Endereco e;
	int qt;
	int indice;
    long qtdRegistros;

	printf("Tamanho da Estrutura: %ld\n\n", sizeof(Endereco));
    
	cepNormal = fopen("cep.dat","rb");
    escrita = fopen("indice.dat","wb");
    fseek(cepNormal,0,SEEK_END);
    qtdRegistros = ftell(cepNormal)/sizeof(Endereco)-1;
    rewind(cepNormal);
    
    //cria um "array" de struct
    CEP *cepIndice;
    //aloca o tamanho total do registros * tamanho de uma estrutura cep para o array.
    cepIndice = malloc(qtdRegistros*sizeof(CEP));
    
    qt = fread(&e,sizeof(Endereco),1,cepNormal);
	indice = 0;
    
	while(qt > 0)
	{
        strncpy(cepIndice[indice].cep,e.cep,8);
        cepIndice[indice].indice = indice;
        qt = fread(&e,sizeof(Endereco),1,cepNormal);
        indice++;
	}
	fclose(cepNormal);
    qsort(cepIndice,qtdRegistros,sizeof(CEP),compara);
	printf("Ordenado = OK\n");
    escrita = fopen("indice.dat","wb");
	fwrite(cepIndice,sizeof(cepIndice),qtdRegistros,escrita);
	fclose(escrita);
	printf("Escrito = OK\n");
    free(cepIndice);
    return 0;
}