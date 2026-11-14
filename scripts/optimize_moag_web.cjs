const {NodeIO}=require('@gltf-transform/core');
const {ALL_EXTENSIONS,KHRDracoMeshCompression}=require('@gltf-transform/extensions');
const {dedup,flatten,join,weld,prune,textureCompress,compactPrimitive}=require('@gltf-transform/functions');
const {MeshoptSimplifier}=require('meshoptimizer');
const sharp=require('sharp'),draco=require('draco3dgltf');
(async()=>{
 await MeshoptSimplifier.ready;
 const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'draco3d.encoder':await draco.createEncoderModule()});
 const doc=await io.read(process.argv[2]);
 await doc.transform(dedup(),flatten(),join(),weld());
 let before=0,after=0;
 for(const mesh of doc.getRoot().listMeshes())for(const p of mesh.listPrimitives()){
 const ix=p.getIndices();if(!ix)continue;
 const pos=p.getAttribute('POSITION'),n=p.getAttribute('NORMAL');if(!n)continue;
 const inds=new Uint32Array(ix.getArray());before+=inds.length/3;
 const [out,error]=MeshoptSimplifier.simplifyWithAttributes(inds,new Float32Array(pos.getArray()),3,new Float32Array(n.getArray()),3,[.03,.03,.03],null,Math.floor(inds.length*.16/3)*3,.00005,[]);
 p.setIndices(doc.createAccessor().setType('SCALAR').setArray(out).setBuffer(ix.getBuffer()));compactPrimitive(p);after+=out.length/3;
 }
 await doc.transform(prune(),textureCompress({encoder:sharp,targetFormat:'webp',resize:[1024,1024]}));
 doc.createExtension(KHRDracoMeshCompression).setRequired(true).setEncoderOptions({method:KHRDracoMeshCompression.EncoderMethod.EDGEBREAKER,encodeSpeed:5,decodeSpeed:7,quantizationBits:{POSITION:20,NORMAL:14,TEX_COORD:16,COLOR:8,GENERIC:16},quantizationVolume:'scene'});
 await io.write(process.argv[3],doc);console.log({before,after});
})().catch(e=>{console.error(e);process.exit(1)});
