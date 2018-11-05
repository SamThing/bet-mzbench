# Ajustes MZBench

MZBench é uma ferramenta expressiva e escalável para testes de carga.
Foi desenvolvida para ajudar os desenvolvedores para testar softwares com uma enorme carga de dados reduzindo assim os riscos em produção.
A documentação do MZBench pode ser encontrada [aqui](https://satori-com.github.io/mzbench/).

O pessoal do VerneMQ desenvolveu um plugin/worker para o MZBench para que se possa desenvolver facilmente _scenarios_ que interagem com servidores MQTT.
Mais informações sobre este plugin pode ser encontrado [aqui](https://vernemq.com/blog/2016/08/26/loadtesting-mqtt-brokers.html).

Este repositório ajusta o Docker do MZBench para que possamos executa-lo na AWS com clientes em instancias EC2.
O MZBench possui alguns Cloud Plugins nativos, entre eles um plugin para suporte ao EC2 da AWS.

# Build

Para gerar a imagem com os ajustes necessários, execute os comandos abaixo estand no subdiretório mzbench deste repositório:

```bash
# Baixe o repositório atual do MZBench
git clone https://github.com/machinezone/mzbench

<<<<<<< HEAD
# Copie as customizacoes necessários
cp -r tp_customizations/* mzbench/
=======
# Copie os arquivos necessários
cp Dockerfile mzbench/
cp -r config mzbench/
cp <local do arquivo tp-general-purpose.pem> mzbench
>>>>>>> 68bcb00347c953ba41eb3c8d6be619595def2110

# Acessa o diretorio do código do mzbench
cd mzbench

# Gere a imagem do docker
docker build -t tp/mzbench .

# TODO: Enviar a imagem para o ECR (Amazon Elastic Container Registry).
```

Para testar se a imagem foi gerada corretamente, execute:

```bash
docker run -d -p 4800:80 --name mzbench_server tp/mzbench
```

Agora acesse http://localhost:4800/.

aws ec2 request-spot-fleet --spot-fleet-request-config file://full_aws_spot_config.json