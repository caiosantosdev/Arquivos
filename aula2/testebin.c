#include<stdio.h>
#include<string.h>

typedef struct _Pessoa Pessoa;
struct _Pessoa {
    char nome[40];
    int idade;
    float altura;
};

int main(){
    FILE *f = fopen("saida.dat","wb");
    Pessoa p;
    strcpy(p.nome, "Renato Mauro");
    p.idade = 49;
    p.altura = 1.84;
    fwrite(&p, sizeof(Pessoa), 1, f);
    fclose(f);
    return 0;
}