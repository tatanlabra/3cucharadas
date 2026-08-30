import { describe, expect, it } from "vitest";
import { palette, positionFor, type GraphNode } from "../../assets/src/memoria_gobernada/layout";

const node = (source_kind: GraphNode["source_kind"]): GraphNode => ({
  id: `${source_kind}_node`, label: "Nodo agregado", source_kind, scope: "test",
  status: "vigente", observed_at: "2026-08-28T00:00:00Z", provenance: "fixture"
});

describe("memory observatory layout", () => {
  it("keeps source clusters deterministic and distinct", () => {
    expect(positionFor(node("rag"), 1)).toEqual(positionFor(node("rag"), 1));
    expect(positionFor(node("rag"), 1)).not.toEqual(positionFor(node("mail"), 1));
    expect(positionFor(node("thesis"), 1)).not.toEqual(positionFor(node("mail"), 1));
  });

  it("defines a visible color for every source", () => {
    expect(Object.values(palette)).toHaveLength(3);
    expect(Object.values(palette).every((color) => color.startsWith("#"))).toBe(true);
  });
});
