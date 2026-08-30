export type SourceKind = "rag" | "mail" | "thesis";

export type GraphNode = {
  id: string;
  label: string;
  source_kind: SourceKind;
  scope: string;
  status: string;
  observed_at: string;
  provenance: string;
};

const cluster = {
  rag: [0, 1.15, 0],
  mail: [-2.15, -0.65, 0.7],
  thesis: [2.15, -0.65, -0.7]
} as const;

export const palette: Record<SourceKind, string> = {
  rag: "#37e7ff",
  mail: "#ff4fd8",
  thesis: "#b8ff3c"
};

export function positionFor(node: GraphNode, index: number): [number, number, number] {
  const base = cluster[node.source_kind];
  const theta = index * 2.399963229728653;
  const radius = 0.28 + (index % 3) * 0.09;
  return [
    base[0] + Math.cos(theta) * radius,
    base[1] + Math.sin(theta * 1.7) * radius,
    base[2] + Math.sin(theta) * radius
  ];
}
