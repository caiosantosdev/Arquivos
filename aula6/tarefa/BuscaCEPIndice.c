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
	char lixo[2]; // Ao Espaço no final da linha + quebra de linha
};

typedef struct _Indice Indice;

struct _Indice
{
	char cep[8];
    int posicao;
};

int compara(const void *e1, const void *e2)
{
	return strncmp(((Indice*)e1)->cep,((Indice*)e2)->cep,8);
}

int main(int argc, char**argv)
{
	FILE *f;
	Endereco e;
    Indice ind;
	int qt;
	int c = 0;
    int inicio, fim, meio, posicao;

	if(argc != 2)
	{
		fprintf(stderr, "USO: %s [CEP]", argv[0]);
		return 1;
	}

    f = fopen("indice.dat", "rb");
    inicio = 0;
    fseek(f,0,SEEK_END);
    fim = ftell(f)/sizeof(Indice)-1;
    rewind(f);
    posicao = -1;
    while(inicio <= fim) {
        c++;
        meio = (inicio+fim)/2;
        fseek(f,meio*sizeof(Indice),SEEK_SET);
        fread(&ind,sizeof(Indice),1,f);
        printf("%.8s - %.8s\n", argv[1], ind.cep);
        if(strncmp(argv[1],ind.cep,8)==0) {
            posicao = ind.posicao;
            break;
        }
        else {
            if(strncmp(argv[1],ind.cep,8)>0) {
                inicio = meio+1;
            } else {
                fim = meio-1;
            }
        }
    }
    fclose(f);
    if(posicao == -1) {
        printf("Nao achei\n");
    } else {
        f = fopen("cep.dat","rb");
        fseek(f,posicao*sizeof(Endereco),SEEK_SET);
       	fread(&e,sizeof(Endereco),1,f);
        printf("%.72s\n%.72s\n%.72s\n%.72s\n%.2s\n%.8s\n",e.logradouro,e.bairro,e.cidade,e.uf,e.sigla,e.cep);
        fclose(f);
    }
    printf("Comparacoes: %d\n",c);
    return 0;
}

