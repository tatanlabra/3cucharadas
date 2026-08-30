// three@0.185.1 distribuye módulos ESM sin declaraciones en este entorno.
// El visor usa una superficie acotada y mantiene sus tipos de dominio propios.
declare module "three" {
  export const BufferAttribute: any;
  export const BufferGeometry: any;
  export const IcosahedronGeometry: any;
  export const Line: any;
  export const LineBasicMaterial: any;
  export const Mesh: any;
  export const MeshBasicMaterial: any;
  export const PerspectiveCamera: any;
  export const Points: any;
  export const PointsMaterial: any;
  export const Raycaster: any;
  export const Scene: any;
  export const Vector2: any;
  export const Vector3: any;
  export const WebGLRenderer: any;
}
