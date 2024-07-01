# Blender Add-on: Posição da Lua
O posLua é um add-on desenvolvido para o Blender, com o intuito de visualizar a posição da Lua no céu para determinado lugar e tempo. Ele utiliza-se da biblioteca Astropy para calcular os dados astronômicos necessários e, utilizando a API do Blender, cria uma interface que permite o usuário criar a simulação.

## Instalação
### Requisitos
- Blender (4.1.1)
- Python (3,11,7)

### Pacotes e módulos
- [Blender Python API](https://docs.blender.org/api/current/index.html)
- [pip](https://pypi.org/project/pip/)
- [NumPy](https://numpy.org/)
- [Astropy](https://www.astropy.org/)

### Passo a passo
- Instalando o 'pip'
  O ambiente Python do Blender não vem com o 'pip' instalado por padrão, esse pacote permite a instalação dos módulos que precisamos para calcular os dados astronômicos.
  Para instalar o 'pip':
  1. Encontre o caminho da pasta onde está o .exe do Python dentro da pasta de instalação do Blender.
     Para o Windows, utilizando o Blender 4.1, o caminho para a pasta é:
     '''
     C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin
     '''
  2. Abra o prompt de comando como administrador.
     'Win + r' > digite 'cmd' > 'Ctrl + Shift + Enter'
  3. Navegue para o diretório do Python dentro da pasta do Blender.
     '''
     cd "C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin"
     '''
  4. Inicie o Python através do prompt de comando digitando 'python' e depois pressione 'Enter'.
  5. Saia do Python, digitando 'exit()' e pressione 'Enter'.
  6. Digite o comando 'python -m ensurepip' e pressione 'Enter' e aguarde a instalação do pacote 'pip' e suas dependências.
     Mantenha o prompt de comando aberto para a instalação dos módulos, conforme os passos a seguir.

- Instalando os módulos
  Com o 'pip' instalado e o prompt de comando ainda aberto, podemos utilizá-lo para baixar os demais módulos necessários.
  1. NumPy: 'pip -m pip install numpy'
  2. Astropy: 'python -m pip install "astropy[all]"'
 
  Depois que os módulos forem baixados e instalados com sucesso, feche o prompt de comando.

- Instalando o Add-on no Blender
  1. Baixe o arquivo 'posLua.zip'.
  2. Abra o Blender.
  3. No menu superior, vá em 'Edit' > 'Preferences' > 'Add-ons'.
     ![Blender Preferences > Add-ons](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/05e6961d-a743-4a2c-b6f5-7de788886ddd)
  4. Clique em 'Install' e selecione o arquivo '.zip'.
  5. Ative o add-on na lista de add-ons.
     ![Blender Preferences > Add-ons > Activate add-on](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/f8057b0f-68c3-4e88-af73-04e9fa5050ed) 
  6. Pronto! O posLua foi instalado com sucesso e já pode ser utilizado dentro do Blender.
 
## Como usar
O posLua funciona através de um painel lateral, encontrado no Viewport 3D principal, pressionando a tecla 'n'.
![Sidebar > Posição da Lua](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/96aec90d-db8d-4f2d-97db-40a174f82c5f)

Através desse painel é possível:
- Criar uma nova cena, utilizando inputs de texto para definir um local e momento para a coleta das coordenadas. Esses dados são usados para posicionar um sólido nesse espaço, e atribuir a ele um material com emissão de luz, para simular de forma simples a Lua;
- Adicionar uma imagem HDR para criar uma ambientação simples para a cena;
- Controlar a intensidade de iluminação gerada pela imagem HDR;
- Ativar e desativar a visualização do grid, eixos e cursor 3D do Blender, para uma simulação mais limpa.













