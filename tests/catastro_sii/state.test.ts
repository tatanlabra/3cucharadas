import { describe, expect, it } from "vitest";
import { regionCodeForName, toDataCommuneCode, toSharedCommuneCode } from "../../assets/src/catastro_sii/state";

describe("territorial code contract", () => {
  it("normalizes the shared five-digit commune code without altering local records", () => {
    expect(toDataCommuneCode("03202")).toBe("3202");
    expect(toDataCommuneCode("3102")).toBe("3102");
    expect(toSharedCommuneCode("3102")).toBe("03102");
  });

  it("rejects malformed codes and maps the Atacama pilot", () => {
    expect(toDataCommuneCode("32A02")).toBeNull();
    expect(regionCodeForName("Atacama")).toBe("03");
  });
});
