# PDF anonymizer 
Extrair conteúdo de texto de PDF e anonimiza. 

Atributos anonimizados:

* Idade
* Nome paciente
* Nome médico
* Cabeçalho
* Datas
* Região
* Hospital

## Build docker image
```
docker build -t anonymizer .
```

## Execute o container associando a sua pasta de PDF como volume
```
docker run --name anonymizer -v <pdf_directory_full_path>:/PDF anonymizer
```

Exemplo
```
docker run --name anonymizer -v ~/Desktop/PDFs:/PDF anonymizer
```


Será gerado um ficheiro .txt pada cada ficheiro .pdf com o texto anonimizado.