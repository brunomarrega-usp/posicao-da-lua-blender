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
#### Instalando o `pip`
O ambiente Python do Blender não vem com o `pip` instalado por padrão, esse pacote permite a instalação dos módulos que precisamos para calcular os dados astronômicos.
Para instalar o 'pip':
  1. Encontre o caminho da pasta onde está o `.exe` do Python dentro da pasta de instalação do Blender.
     Para o Windows, utilizando o Blender 4.1, o caminho para a pasta é:
     ```
     C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin
     ```
  2. Abra o prompt de comando como administrador.
     `Win + r` > digite `cmd` > `Ctrl + Shift + Enter`
  3. Navegue para o diretório do Python dentro da pasta do Blender.
     ```
     cd "C:\Program Files\Blender Foundation\Blender 4.1\4.1\python\bin"
     ```
  4. Inicie o Python através do prompt de comando digitando `python` e depois pressione `Enter`.
  5. Saia do Python, digitando `exit()` e pressione `Enter`.
  6. Digite o comando `python -m ensurepip` e pressione `Enter` e aguarde a instalação do pacote `pip` e suas dependências.
     Mantenha o prompt de comando aberto para a instalação dos módulos, conforme os passos a seguir.

#### Instalando os módulos
  Com o `pip` instalado e o prompt de comando ainda aberto, podemos utilizá-lo para baixar os demais módulos necessários.
  1. NumPy: `pip -m pip install numpy`
  2. Astropy: `python -m pip install "astropy[all]"`
 
  Depois que os módulos forem baixados e instalados com sucesso, feche o prompt de comando.

#### Instalando o Add-on no Blender
  1. Baixe o arquivo `posLua.zip`.
  2. Abra o Blender.
  3. No menu superior, vá em `Edit` > `Preferences` > `Add-ons`.
     ![Blender Preferences > Add-ons](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/05e6961d-a743-4a2c-b6f5-7de788886ddd)
  4. Clique em `Install` e selecione o arquivo `.zip`.
  5. Ative o add-on na lista de add-ons.
     ![Blender Preferences > Add-ons > Activate add-on](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/f8057b0f-68c3-4e88-af73-04e9fa5050ed) 
  6. Pronto! O posLua foi instalado com sucesso e já pode ser utilizado dentro do Blender.
 
## Como usar
O posLua funciona através de um painel lateral, encontrado no Viewport 3D principal, pressionando a tecla `n`.
![Sidebar > Posição da Lua](https://github.com/brunomarrega-usp/posicao-da-lua-blender/assets/165938265/96aec90d-db8d-4f2d-97db-40a174f82c5f)

Através desse painel é possível:
- Criar uma nova cena, utilizando inputs de texto para definir um local e momento para a coleta das coordenadas. Esses dados são usados para posicionar um sólido nesse espaço, e atribuir a ele um material com emissão de luz, para simular de forma simples a Lua;
- Adicionar uma imagem HDR para criar uma ambientação simples para a cena;
- Controlar a intensidade de iluminação gerada pela imagem HDR;
- Ativar e desativar a visualização do grid, eixos e cursor 3D do Blender, para uma simulação mais limpa.

### Criando uma nova simulação
No Viewport, abra a barra lateral pressionando `n` e entre na aba `Posição da Lua` e proceda conforme a ordem dos passos descritos no painel.
- Passo 1: Criar cena
  1. Uma janela pop-up surgirá pedindo que sejam fornecidos o tempo e o local
  2. A cena é criada, com a representação da Lua posicionada conforme as coordenadas calculadas.
- Passo 2: Importar HDR
  1. Uma janela surgirá para importar uma imagem ([HDRi](https://christianezhao.medium.com/everything-you-need-to-know-about-an-hdr-panorama-image-ee5953073b6a)) que será usada de fundo
  2. Através do slider à direita, controla-se a intensidade da iluminação proveniente da imagem
- Ver grid: chackbox que controla a exibição da malha, eixos e cursor 3D

> [!NOTE]
> Sempre que uma nova cena é criada, o espaço é resetado.

## Como tudo funciona
Para funcionar como um add-on dentro do Blender, a notação empregada foi a tradicionalmente utilizada para as classes de operadores e paineis, como é indicado na documentação do módulo `bpy`. O bloco inicial contém informações para registro do script, a versão mínima do Blender, autores e outras informações do add-on:
```python
bl_info = {
    "name": "Posição da Lua",
    "author": "Bruno Marrega, Gabriela Bezerra, Kevin Akihito, Samara Amorin",
    "version": (0, 0, 1),
    "blender": (4, 1, 1),
    "location": "3D Viewport > Sidebar > Posição da Lua",
    "description": "Simulador da posição da Lua",
    "category": "Simulation",
}
```
### Coordenadas cartesianas
```python
def coordCartesianas_lua(cidade, tempo):
    # Localização do observador
    loc = apc.EarthLocation.of_address(cidade)

    # Tempo da observação
    t = apt.Time(tempo)
              
    # AltAz frame (altitude e azimute) para o local e tempo definidos
    altaz_frame = apc.AltAz(obstime=t, location=loc)

    # Altitude e azimute da Lua
    altaz_lua = apc.get_body('moon', t, loc).transform_to(altaz_frame)
              
    # Altitude (alt) é o ângulo de elevação a partir do horizonte
    # Azimute (az) é o ângulo medido em sentido horário a partir do norte
    alt = altaz_lua.alt.rad
    az = altaz_lua.az.rad

    # Converter coordenadas esféricas (alt, az) para coordenadas cartesianas (x, y, z)
    x = np.cos(alt) * np.cos(az) * 1000
    y = np.cos(alt) * np.sin(az) * 1000
    z = np.sin(alt) * 1000
         
    return x, y, z
```
A função consulta a altitude e azimute através do módulo Astropy, e converte essas coordenadas para cartesianas, retornando o `x`, `y` e `z` para a Lua, para aquele momento, naquele lugar. Essa função será utilizada posteriormente dentro da classe que opera a função do botão `Criar cena`.

### Limpar cena
```python
def limpar_cena():
    """Limpa todos os objetos e materiais da cena"""
    
    # Deleta todos os objetos dentro da cena
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Acessa e deleta todos os materiais
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)
    
    # Cria um novo mundo, caso nao exista
    if not bpy.data.worlds:
        bpy.data.worlds.new("World")
    world = bpy.data.worlds[0]
        
    # Limpa todos os nodes existentes
    world.node_tree.nodes.clear()
```
Para não sobrepor as cenas com objetos repetidos a cada iteração com o botão `Criar cena`, é configurada uma função que limpa todas as informações da cena atual. Essa função será chama sempre que uma nova cena é criada, antes de qualquer outra função.

### Operadores
De acordo com a [documentação do Blender]([https://developer.blender.org/docs/](https://developer.blender.org/docs/features/interface/operators/)), operadores são classes que executam funções com funcionalidades adicionais e configurações de entrada. Se um atalho ou botão for pressionado, geralmente isso chama um operador. Por convenção: `CATEGORIA_OT_nome`.
Para esse script, foram utulizados três operadores:
- `MESH_OT_criar_lua` para criar a representação da Lua e posicioná-la em uma nova cena.
- `RENDER_OT_hdri` para atribuir uma imagem HDR importada ao ambiente.
- `VIEW_OT_toggle_grid` para alternar a vizibilidade do grid.





