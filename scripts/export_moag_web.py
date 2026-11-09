"""Derive a web-only glTF from v05; never save over the Blender master."""
import bpy, json, sys, hashlib
import numpy as np
from pathlib import Path
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
ROOT=args.output.resolve();ROOT.mkdir(parents=True,exist_ok=True)
SOURCE=args.source.resolve()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),load_ui=False,use_scripts=False)
# Direct glTF-compatible materials. Bake the subtle albedo tint into small tiled maps.
# Blender's procedural node graphs and Cycles lights do not transfer to glTF.
means={'ceramic':(.726,.681,.659),'titanium':(.36,.365,.37),'graphite':(.035,.039,.047)}
roughmeans={'ceramic':.40,'titanium':.28,'graphite':.52}
pixel_cache={}
for im in list(bpy.data.images):
 if im.source=='FILE':
  im.scale(1024,576)
  a=np.empty(1024*576*4,dtype=np.float32);im.pixels.foreach_get(a);pixel_cache[im.name]=a.reshape(576,1024,4).copy()

def bitmap(name,a,color):
 im=bpy.data.images.new(name,1024,576,alpha=False);im.colorspace_settings.name=color;im.pixels.foreach_set(a.ravel());im.pack();return im

for mat in bpy.data.materials:
 if not mat.use_nodes:continue
 nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
 defaults={key:bs.inputs[key].default_value for key in ['Metallic','Roughness','Emission Strength','Transmission Weight']}
 base=tuple(bs.inputs['Base Color'].default_value);emission=tuple(bs.inputs['Emission Color'].default_value)
 old_images={n.image.name:n.image for n in nt.nodes if n.type=='TEX_IMAGE' and n.image}
 family=next((f for f in means if f+'_basecolor_4k.png' in old_images),None)
 calm=nt.nodes.get('PBR_Subtle_Albedo')
 mix=float(calm.inputs[0].default_value) if calm else .12
 if calm:base=tuple(calm.inputs[1].default_value)
 roughscale=1
 if bs.inputs['Roughness'].is_linked:
  n=bs.inputs['Roughness'].links[0].from_node
  if n.type=='MATH' and n.operation=='MULTIPLY':roughscale=n.inputs[1].default_value
 normalstrength=.12
 nt.nodes.clear();bs=nt.nodes.new('ShaderNodeBsdfPrincipled');out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
 bs.inputs['Base Color'].default_value=base;bs.inputs['Emission Color'].default_value=emission
 for k,v in defaults.items():bs.inputs[k].default_value=v
 # Small cabin panes use opaque reflective glass for stable real-time visibility.
 if 'Cabin' in mat.name:bs.inputs['Transmission Weight'].default_value=0
 def tex(im):
  n=nt.nodes.new('ShaderNodeTexImage');n.image=im;n.extension='MIRROR';return n
 if family:
  a=pixel_cache[family+'_basecolor_4k.png'].copy()
  a[:,:,:3]=np.clip((1-mix)*np.array(base[:3])+mix*a[:,:,:3]*np.array(base[:3])/np.array(means[family]),0,1)
  nt.links.new(tex(bitmap(mat.name+'_Albedo',a,'sRGB')).outputs['Color'],bs.inputs['Base Color'])
  rough=pixel_cache[family+'_roughness_4k.png'].copy();rough[:,:,:3]=np.clip(rough[:,:,:3]*roughscale,0,1)
  nt.links.new(tex(bitmap(mat.name+'_Roughness',rough,'Non-Color')).outputs['Color'],bs.inputs['Roughness'])
  bs.inputs['Metallic'].default_value=float(pixel_cache[family+'_metallic_4k.png'][:,:,0].mean())
  normal=nt.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.12
  nt.links.new(tex(old_images[family+'_normal_opengl_4k.png']).outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs[0],bs.inputs['Normal'])
 elif 'glass_roughness_4k.png' in old_images:
  nt.links.new(tex(old_images['glass_roughness_4k.png']).outputs['Color'],bs.inputs['Roughness'])

bpy.ops.object.select_all(action='DESELECT')
counts=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH' and not o.hide_render:
  o.hide_set(False);o.hide_viewport=False;o.select_set(True)
  # One canonical UV channel; remove redundant attributes before export.
  if o.data.uv_layers:
   keep=o.data.uv_layers.get('SurfaceUV') or o.data.uv_layers.active
   for uv in list(o.data.uv_layers):
    if uv!=keep:o.data.uv_layers.remove(uv)
   keep.active_render=True
  o.data.calc_loop_triangles();counts.append({'name':o.name,'triangles':len(o.data.loop_triangles)})
print('EXPORT_START',sum(x['triangles'] for x in counts),flush=True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'moag041-v05-raw.glb'),export_format='GLB',use_selection=True,export_animations=False,export_cameras=False,export_lights=False,export_extras=False,export_apply=True,export_image_format='JPEG',export_jpeg_quality=86,export_image_quality=86,export_texcoords=True,export_normals=True,export_tangents=False,export_vertex_color='NONE')
(ROOT/'export_source.json').write_text(json.dumps({'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source_version':'v05','source_triangles':sum(x['triangles'] for x in counts),'texture_web_size':[1024,576],'meshes':counts},indent=2))
print('WEB_EXPORT_COMPLETE',flush=True)
