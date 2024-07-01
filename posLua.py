bl_info = {
    "name": "Posição da Lua",
    "author": "Bruno Marrega, Gabriela Bezerra, Kevin Akihito, Samara Amorim",
    "version": (0, 0, 1),
    "blender": (4, 1, 1),
    "location": "3D Viewport > Sidebar > Posição da Lua",
    "description": "Simulador da posição da Lua",
    "category": "Simulation",
} # Informações para registro do Add-on


import bpy
from bpy.types import (Panel, Operator)

import numpy as np
from astropy import coordinates as apc
from astropy import time as apt
from astropy import units as u



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


#----------------------------------------------------------------------------------------
#-------------------------------    OPERADORES    ---------------------------------------
#----------------------------------------------------------------------------------------
class MESH_OT_criar_lua(bpy.types.Operator):    # Convençao de nome: CATEGORIA_OT_nome
    """
    Cria uma nova cena simulando a posição da Lua no céu,
    de acordo com o modulo Astropy.
    """
    
    # ID do operador
    bl_idname = "mesh.criar_lua" 
    bl_label = "Defina o local e o momento, conforme os formatos indicados:"
    
    # Inputs de texto para o dialog box
                            ################## Verificar a validade das strings!
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
        
        print(tempo,cidade)
        
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


class RENDER_OT_hdri(bpy.types.Operator):
    """
    Configura uma ambientação mais realista e permite a utilização
    de um HDRi para o background
    """  
    
    # ID do operador
    bl_idname = "render.hdri" 
    bl_label = "Importe o arquivo HDR para o backgrOund"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    strength: bpy.props.FloatProperty(name="Intensidade", default=1.0, min=0.0)
    
    def execute(self, context):
        # Seleciona o mundo existente
        world = bpy.data.worlds[0]
        bpy.context.scene.world = world
        
        # Cria uma nova cadeia de nodes
        if world.use_nodes is False:
            world.use_nodes = True
        
        # Limpa os nodes existentes
        world.node_tree.nodes.clear()
        
        # Adiciona os nodes de textura do background e do ambiente
        node_tree = world.node_tree
        bg_node = node_tree.nodes.new(type="ShaderNodeBackground")
        env_texture_node = node_tree.nodes.new(type="ShaderNodeTexEnvironment")
        
        # Carrega a imagem importada
        env_texture_node.image = bpy.data.images.load(self.filepath)
        
        # Set the strength of the background node
        bg_node.inputs['Strength'].default_value = self.strength
        
        # Cria o node de output
        output_node = node_tree.nodes.new(type="ShaderNodeOutputWorld")
        
        # Liga os nodes
        node_tree.links.new(env_texture_node.outputs["Color"], bg_node.inputs["Color"])
        node_tree.links.new(bg_node.outputs["Background"], output_node.inputs["Surface"])

        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW_OT_toggle_grid(bpy.types.Operator):
    """Toggle para a malha de fundo"""
    bl_idname = "view.grid"
    bl_label = "Ver grid de fundo"
    
    def execute(self, context):
        bpy.context.space_data.overlay.show_ortho_grid = not bpy.context.space_data.overlay.show_ortho_grid
        bpy.context.space_data.overlay.show_floor = not bpy.context.space_data.overlay.show_floor
        
        bpy.context.space_data.overlay.show_axis_x = not bpy.context.space_data.overlay.show_axis_x
        bpy.context.space_data.overlay.show_axis_y = not bpy.context.space_data.overlay.show_axis_y
        bpy.context.space_data.overlay.show_axis_z = not bpy.context.space_data.overlay.show_axis_z
        
        bpy.context.space_data.overlay.show_cursor = not bpy.context.space_data.overlay.show_cursor

        return {'FINISHED'}
    
    

#----------------------------------------------------------------------------------------
#--------------------------------      PAINEL      --------------------------------------
#----------------------------------------------------------------------------------------
class VIEW3D_PT_posicaoLua(bpy.types.Panel):    # Convençao de nome: CATEGORIA_PT_nome
    """Cria um painel com o input de texto e um botão simples"""
    
    # Onde estará o painel dentro da interface
    bl_space_type = 'VIEW_3D'         # 3d Viewport
    bl_region_type = 'UI'             # Barra lateral
    
    # Labels
    bl_category = "Posição da Lua"    # Nome que aparecerá na barra lateral
    bl_idname = "OBJECT_PT_posLua"    # ID do painel
    bl_label = "Posição da Lua"       # Texto no topo do painel
    
    
    def draw(self, context):
        """Define o layout do painel"""
        layout = self.layout
        layout.label(text="Passo 1:")
        layout.operator("mesh.criar_lua", text="Criar cena", icon='PHYSICS')
        
        layout.label(text="Passo 2:")
        row = layout.row()
        
        col1 = row.column()
        col1.operator("render.hdri", text="Importar HDR", icon='WORLD')
        
        # Slider para a intensidade
        col2 = row.column()
        col2.prop(context.scene, "hdr_img_a", text="Intensidade")
        
        # Toggle para o grid
        layout.prop(context.scene, "ver_grid", text="Ver grid")
        
        layout.scale_y = 1.2


def atualiza_hdri_a(self, context):
    """
    Encontra o atributo 'Strength' da imagem HDR importada
    e linka o slider do painel a ela
    """
    
    world = context.scene.world
    if world and world.node_tree:
        bg_node = world.node_tree.nodes.get('Background')
        if bg_node:
            bg_node.inputs['Strength'].default_value = context.scene.hdr_img_a


def update_ver_grid(self, context):
    bpy.context.space_data.overlay.show_ortho_grid = bpy.context.space_data.overlay.show_floor = bpy.context.space_data.overlay.show_axis_x = bpy.context.space_data.overlay.show_axis_y = bpy.context.space_data.overlay.show_axis_z = bpy.context.space_data.overlay.show_cursor =  context.scene.ver_grid


#----------------------------------------------------------------------------------------
#---------------------------------     REGISTRO     -------------------------------------
#----------------------------------------------------------------------------------------
# Registro do painel e dos operadores no Blender
from bpy.utils import register_class, unregister_class

_classes = [
    MESH_OT_criar_lua,
    RENDER_OT_hdri,
    VIEW_OT_toggle_grid,
    VIEW3D_PT_posicaoLua
]

def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.hdr_img_a = bpy.props.FloatProperty(
        name="Intensidade da Imagem HDR",
        description="Intensidade da luz da imagem HDR de fundo",
        default=1.0,
        min=0.0,
        update=atualiza_hdri_a
    )
    
    bpy.types.Scene.ver_grid = bpy.props.BoolProperty(
        name="Ver grid",
        description="Muda a visibilidade do grid de fundo",
        default=True,
        update=update_ver_grid
    )


def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.hdr_image_strength
    del bpy.types.Scene.ver_grid

if __name__ == "__main__":
    register()
