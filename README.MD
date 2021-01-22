# PDF anonymizer 


Defina um diretório com os ficheiros PDF (ex:/path/to/pdf/folder)

## Build docker image
sudo docker build -t anonymizer /path/to/pdf/folder

## Execute o container associando a sua pasta de PDF como volume
sudo docker run -v /path/to/pdf/folder:/PDF anonymizer

