r : Abre o arquivo para leitura. Se não for encontrado, a abertura dará um erro. O ponteiro de leitura começa no início do arquivo.

w: abre o arquivo somente para escrita. Se o arquivo possuir conteúdo, seu conteúdo será apagado. Se o arquivo não existir, será criado. O ponteiro começa no início do arquivo.

a: Abre o arquivo para escrita no final (append). Se o arquivo não existir, será criado.

r+: Abre o arquivo com as funções de leitura e escrita. Se o arquivo não existir será dado um erro.

w+: Cria um novo arquivo para escrita e leitura. Se o arquivo existir, o conteúdo anterior será destruído. Se não existir, será criado.

r+b: Abre um arquivo binário para leitura e escrita. O mesmo que "r+" acima, só que o arquivo é binário.

rb: Abre um arquivo para leitura em binário.