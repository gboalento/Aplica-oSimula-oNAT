# Simulação do Funcionamento do NAT
Criamos uma aplicação em Python que simula um tráfego entre duas redes distintas e usamos um script dentro da aplicação para observar o funcionamento do NAT. Criamos um dashboard em HTML para observar a gerencia do NAT nos IP's publicos e privados. Podemos observar quadro colunas ao rodar a aplicação, sendo elas o IP privado e o IP publico de saida do pacote da rede 1 para a rede 2, com seu IP publico e IP privado (Global e Local Entry; Global e Local Exit).

## Requisitos

- Python 3.12 ou superior
- Bibliotecas Python:
  - scapy
  - flask
  - dash
  - dash-bootstrap-components

 ## Passo a passo

- Instale o python em seu computador e durante a instalação, marque a opção "Add Python to PATH"
- Cria uma pasta e coloque os arquivos requirements.txt, 'nat_simulation.py' e 'app.py'
- Instale as bibliotecas necessárias. Para isso no prompt de comando no local onde foi instalado o python, execute o comando: pip install -r requirements.txt  
- Após isso você estará hábil a rodar o script
- Novamente no prompt, rode o script com o comando: python app.py
- Abra o navegador e vá para http://127.0.0.1:8050/ para visualizar o dashboard em tempo real.
