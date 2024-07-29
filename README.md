# Blender Add-on: Posição da Lua
O posLua é um add-on desenvolvido para o Blender, com o intuito de visualizar a posição da Lua no céu para determinado lugar e tempo. Ele utiliza-se da biblioteca Astropy para calcular os dados astronômicos necessários e, utilizando a API do Blender, cria uma interface que permite o usuário criar a simulação.

## Instalação
### Requisitos
- Blender (4.1.1)
- Python (3.11.7)

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
  1. NumPy: `python -m pip install numpy`
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
De acordo com a [documentação do Blender](https://developer.blender.org/docs/features/interface/operators/), operadores são classes que executam funções com funcionalidades adicionais e configurações de entrada. Se um atalho ou botão for pressionado, geralmente isso chama um operador. Por convenção: `CATEGORIA_OT_nome`.
Para esse script, foram utulizados três operadores:
- `MESH_OT_criar_lua` para criar a representação da Lua e posicioná-la em uma nova cena.
- `RENDER_OT_hdri` para atribuir uma imagem HDR importada ao ambiente.
- `VIEW_OT_toggle_grid` para alternar a vizibilidade do grid.

#### `MESH_OT_criar_lua`
```python
class MESH_OT_criar_lua(bpy.types.Operator):
    """
    Cria uma nova cena simulando a posição da Lua no céu,
    de acordo com o modulo Astropy.
    """

    # ID do operador
    bl_idname = "mesh.criar_lua"
    bl_label = "Defina o local e o momento, conforme os formatos indicados:"

    # Inputs de texto para o dialog box
    str_tempo: bpy.props.StringProperty(name="Tempo:", default="2024-01-30 01:05")
    str_local: bpy.props.StringProperty(name="Local:", default="Lorena, São Paulo, Brazil")


    def execute(self, context):
        # Deletar todos os objetos da cena
        limpar_cena()

        # Cor de fundo
        bpy.context.preferences.themes[0].view_3d.space.gradients.high_gradient = (0, 0, 0)

        # Resetar a posição do cursor 3D para a origem
        bpy.context.scene.cursor.location = (0, 0, 0)

        # ----- Coordenadas ----- #
        # Definir a data e localização para as coordenadas
        tempo = self.str_tempo
        cidade = self.str_local

        x, y, z = coordCartesianas_lua(cidade, tempo)

        # Cria uma esfera e atribui um nome a ela
        bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, align='WORLD', location=(x, y, x), scale=(20, 20, 20))
        lua = context.active_object
        lua.name = "Lua"

        # ----- Material ----- #        
        # Criar novo material
        material_lua = bpy.data.materials.new(name="matLua")
        material_lua.use_nodes = True

        # Criar shader de emissão de luz
        bpy.data.materials["matLua"].node_tree.nodes["Principled BSDF"].inputs[27].default_value = 10
        bpy.data.materials["matLua"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.52, 0.50, 0.67, 1)

        # Configurar renderizador
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

        # Permitir a função bloom)
        bpy.context.scene.eevee.use_bloom = True

        # Definir o tipo de shading
        bpy.context.space_data.shading.type = 'RENDERED'

        # Atribuir material à "Lua"
        lua.active_material = material_lua    

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
```
Essa classe cria um operador que abre uma caixa de diálogo quando invocado, pedindo dois _inputs_ em formato `string`, uma para o tempo e outra para o local, armazenadas, respectivamente em `self.str_tempo` e `self.str_local`. Essas variáveis são usadas como argumentos para chamar a função `coordCartesianas_lua` definida anteriormente, e que retorna três valores para posição, guardados nas variáveis locais `x`, `y` e `z`.

Chamando a função `bpy.ops.mesh.primitive_ico_sphere_add`, própria da API do Blender, criamos uma nova Icoesfera, usando como argumento para sua posição as variáveis definidas acima. Depois, tornamos essa esfera o objeto ativo na cena em contexto e atribuímos a ela o nome `Lua`.

Com o objeto ativo na cena, criamos um novo material chamado de `matLua`, amarrado à variável `material_lua`, e definimos alguns parâmetros basicos para seus _[shaders](https://en.wikipedia.org/wiki/Shader)_, um material de cor branca e emissão de luz.

Para que essa emissão de luz possa ser vista em tempo real utilizando o _viewport_ do Blender, sem que haja a necessidade de renderizar a cena, definimos que o mecanismo de renderização será o Eevee com: `bpy.context.scene.render.engine = 'BLENDER_EEVEE'`, permitimos o uso do efeito _bloom_ e configuramos o tipo de vizualização do _viewport_ para `RENDERED`.
