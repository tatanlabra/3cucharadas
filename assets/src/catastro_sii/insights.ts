import type {
  CommuneInsight,
  InsightsV1,
  PipelineLink,
  PipelineNode,
  SensitivityRow,
  ViolinGroup,
  ViolinPanel
} from "./types";

export const INSIGHTS_URL = "/catastro_sii_brecha/data/insights-v1.json";
export const LEGACY_COMMUNES_URL = "/catastro_sii_brecha/data/explorador_comunal.json";

type JsonObject = Record<string, unknown>;

export type InsightsLoadResult =
  | { source: "v1"; data: InsightsV1; communes: CommuneInsight[]; warning: null }
  | { source: "legacy"; data: null; communes: CommuneInsight[]; warning: string };

function object(value: unknown, path: string): JsonObject {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${path} debe ser un objeto`);
  return value as JsonObject;
}

function string(value: unknown, path: string): string {
  if (typeof value !== "string" || !value.trim()) throw new Error(`${path} debe ser texto no vacío`);
  return value;
}

function number(value: unknown, path: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) throw new Error(`${path} debe ser un número finito`);
  return value;
}

function nullableNumber(value: unknown, path: string): number | null {
  return value == null ? null : number(value, path);
}

function array(value: unknown, path: string): unknown[] {
  if (!Array.isArray(value)) throw new Error(`${path} debe ser una lista`);
  return value;
}

function parsePipelineNode(value: unknown, index: number): PipelineNode {
  const item = object(value, `pipeline.nodes[${index}]`);
  const unit = string(item.unit, `pipeline.nodes[${index}].unit`);
  if (unit !== "records" && unit !== "properties") throw new Error("pipeline distingue records de properties");
  return {
    id: string(item.id, `pipeline.nodes[${index}].id`),
    label: string(item.label, `pipeline.nodes[${index}].label`),
    value: number(item.value, `pipeline.nodes[${index}].value`),
    unit
  };
}

function parsePipelineLink(value: unknown, index: number): PipelineLink {
  const item = object(value, `pipeline.links[${index}]`);
  return {
    source: string(item.source, `pipeline.links[${index}].source`),
    target: string(item.target, `pipeline.links[${index}].target`),
    value: number(item.value, `pipeline.links[${index}].value`)
  };
}

function parseViolinGroup(value: unknown, path: string): ViolinGroup {
  const item = object(value, path);
  const points = array(item.points, `${path}.points`).map((point, index) => {
    const pair = array(point, `${path}.points[${index}]`);
    if (pair.length !== 2) throw new Error(`${path}.points[${index}] debe contener valor y densidad`);
    return [number(pair[0], `${path}.points[${index}][0]`), number(pair[1], `${path}.points[${index}][1]`)] as [number, number];
  });
  const quartile = number(item.quartile, `${path}.quartile`);
  if (!Number.isInteger(quartile) || quartile < 1 || quartile > 4) throw new Error(`${path}.quartile fuera de 1..4`);
  if (points.length < 2) throw new Error(`${path}.points requiere al menos dos puntos`);
  return {
    quartile,
    n: number(item.n, `${path}.n`),
    min: number(item.min, `${path}.min`),
    q1: number(item.q1, `${path}.q1`),
    median: number(item.median, `${path}.median`),
    q3: number(item.q3, `${path}.q3`),
    max: number(item.max, `${path}.max`),
    points
  };
}

function parseViolinPanel(value: unknown, index: number): ViolinPanel {
  const path = `violin_densities.panels[${index}]`;
  const item = object(value, path);
  const groups = array(item.groups, `${path}.groups`).map((group, groupIndex) => parseViolinGroup(group, `${path}.groups[${groupIndex}]`));
  if (groups.length !== 4 || new Set(groups.map((group) => group.quartile)).size !== 4) {
    throw new Error(`${path}.groups debe cubrir los cuatro cuartiles`);
  }
  return {
    id: string(item.id, `${path}.id`),
    title: string(item.title, `${path}.title`),
    metric: string(item.metric, `${path}.metric`),
    universe: string(item.universe, `${path}.universe`),
    display_scale: item.display_scale === "original" ? "original" : undefined,
    bandwidth_method: typeof item.bandwidth_method === "string" ? item.bandwidth_method : undefined,
    cut: typeof item.cut === "number" ? item.cut : undefined,
    groups
  };
}

function parseSensitivityRow(value: unknown, index: number): SensitivityRow {
  const path = `sensitivity.rows[${index}]`;
  const item = object(value, path);
  const pearson = number(item.pearson, `${path}.pearson`);
  const spearman = number(item.spearman, `${path}.spearman`);
  if (Math.abs(pearson) > 1 || Math.abs(spearman) > 1) throw new Error(`${path}: correlación fuera de [-1, 1]`);
  return {
    id: string(item.id, `${path}.id`),
    label: string(item.label, `${path}.label`),
    n: number(item.n, `${path}.n`),
    pearson,
    spearman,
    universe: string(item.universe, `${path}.universe`)
  };
}

function parseCommune(value: unknown, index: number): CommuneInsight {
  const path = `communes[${index}]`;
  const item = object(value, path);
  const code = string(item.code, `${path}.code`);
  if (!/^\d{4,5}$/.test(code)) throw new Error(`${path}.code inválido`);
  return {
    code,
    name: string(item.name, `${path}.name`),
    region: string(item.region, `${path}.region`),
    vulnerability: nullableNumber(item.vulnerability, `${path}.vulnerability`),
    av_total: nullableNumber(item.av_total, `${path}.av_total`),
    av_household: nullableNumber(item.av_household, `${path}.av_household`),
    av_person: nullableNumber(item.av_person, `${path}.av_person`),
    av_m2: nullableNumber(item.av_m2, `${path}.av_m2`),
    households: nullableNumber(item.households, `${path}.households`),
    urban_pct: nullableNumber(item.urban_pct, `${path}.urban_pct`)
  };
}

const FORBIDDEN_INDIVIDUAL_FIELDS = new Set([
  "qa", "predio", "pred_uid", "rol", "rut", "run", "direccion",
  "avaluo_fiscal_clp", "geometry", "coordinates"
]);

export function containsForbiddenIndividualField(value: unknown): boolean {
  if (Array.isArray(value)) return value.some(containsForbiddenIndividualField);
  if (!value || typeof value !== "object") return false;
  return Object.entries(value as JsonObject).some(([key, nested]) => FORBIDDEN_INDIVIDUAL_FIELDS.has(key) || containsForbiddenIndividualField(nested));
}

/** Valida el artefacto antes de entregar cualquier valor a ECharts. */
export function parseInsightsV1(value: unknown): InsightsV1 {
  const root = object(value, "insights");
  if (root.schema_version !== 1) throw new Error(`schema_version no compatible: ${String(root.schema_version)}`);
  if (containsForbiddenIndividualField(root)) throw new Error("el artefacto contiene un campo predial individual o qa residual");

  const generatedAt = string(root.generated_at, "generated_at");
  if (Number.isNaN(Date.parse(generatedAt))) throw new Error("generated_at no es una fecha válida");
  const sourceHash = string(root.source_hash, "source_hash");
  if (!/^[a-f\d]{64}$/i.test(sourceHash)) throw new Error("source_hash debe ser SHA-256");

  const universeRaw = object(root.universe, "universe");
  const universe = {
    uv: number(universeRaw.uv, "universe.uv"),
    communes: number(universeRaw.communes, "universe.communes"),
    complete_quartiles: number(universeRaw.complete_quartiles, "universe.complete_quartiles"),
    urban_uv: number(universeRaw.urban_uv, "universe.urban_uv")
  };

  const pipelineRaw = object(root.pipeline, "pipeline");
  const nodes = array(pipelineRaw.nodes, "pipeline.nodes").map(parsePipelineNode);
  const links = array(pipelineRaw.links, "pipeline.links").map(parsePipelineLink);
  const ids = new Set(nodes.map((node) => node.id));
  if (!nodes.length || !links.length || links.some((link) => !ids.has(link.source) || !ids.has(link.target))) {
    throw new Error("pipeline contiene enlaces sin nodo o está vacío");
  }

  const violinsRaw = object(root.violin_densities, "violin_densities");
  const panels = array(violinsRaw.panels, "violin_densities.panels").map(parseViolinPanel);
  if (panels.length !== 3) throw new Error("violin_densities debe contener el tríptico de tres paneles");

  const transitionRaw = object(root.quartile_transition, "quartile_transition");
  const matrix = array(transitionRaw.matrix, "quartile_transition.matrix").map((row, rowIndex) => {
    const values = array(row, `quartile_transition.matrix[${rowIndex}]`).map((cell, columnIndex) => number(cell, `quartile_transition.matrix[${rowIndex}][${columnIndex}]`));
    if (values.length !== 4) throw new Error("quartile_transition.matrix debe ser 4×4");
    return values;
  });
  if (matrix.length !== 4) throw new Error("quartile_transition.matrix debe ser 4×4");
  const sameQuartilePct = number(transitionRaw.same_quartile_pct, "quartile_transition.same_quartile_pct");
  const movedTwoPlusPct = number(transitionRaw.moved_two_plus_pct, "quartile_transition.moved_two_plus_pct");
  if ([sameQuartilePct, movedTwoPlusPct].some((item) => item < 0 || item > 100)) throw new Error("porcentaje de transición fuera de 0..100");

  const sensitivityRaw = object(root.sensitivity, "sensitivity");
  const sensitivityRows = array(sensitivityRaw.rows, "sensitivity.rows").map(parseSensitivityRow);
  const communes = array(root.communes, "communes").map(parseCommune);
  if (communes.length !== universe.communes || new Set(communes.map((commune) => commune.code)).size !== communes.length) {
    throw new Error("communes no coincide con el universo o contiene códigos duplicados");
  }

  return {
    schema_version: 1,
    generated_at: generatedAt,
    source_hash: sourceHash,
    universe,
    limits: array(root.limits, "limits").map((limit, index) => string(limit, `limits[${index}]`)),
    pipeline: { nodes, links },
    violin_densities: { panels },
    quartile_transition: {
      matrix,
      same_quartile_pct: sameQuartilePct,
      moved_two_plus_pct: movedTwoPlusPct,
      n: number(transitionRaw.n, "quartile_transition.n")
    },
    sensitivity: { rows: sensitivityRows },
    communes
  };
}

interface LegacyExplorer {
  n?: unknown;
  codigo?: unknown;
  comuna?: unknown;
  region?: unknown;
  series?: unknown;
}

/** Fallback acotado: conserva sólo el gráfico comunal y no inventa denominadores. */
export function parseLegacyCommunes(value: unknown): CommuneInsight[] {
  const raw = object(value, "explorador") as LegacyExplorer;
  const count = number(raw.n, "explorador.n");
  const codes = array(raw.codigo, "explorador.codigo");
  const names = array(raw.comuna, "explorador.comuna");
  const regions = array(raw.region, "explorador.region");
  const series = object(raw.series, "explorador.series");
  const totals = array(series.avaluo_total_mmm, "explorador.series.avaluo_total_mmm");
  const vulnerability = array(series.vulnerabilidad_media, "explorador.series.vulnerabilidad_media");
  const households = array(series.hogares, "explorador.series.hogares");
  const urban = array(series.pct_urbano, "explorador.series.pct_urbano");
  if (![codes, names, regions, totals, vulnerability, households, urban].every((items) => items.length === count)) {
    throw new Error("explorador legacy tiene columnas desalineadas");
  }
  return codes.map((code, index) => ({
    code: string(code, `explorador.codigo[${index}]`),
    name: string(names[index], `explorador.comuna[${index}]`),
    region: string(regions[index], `explorador.region[${index}]`),
    vulnerability: nullableNumber(vulnerability[index], `explorador.vulnerabilidad[${index}]`),
    av_total: nullableNumber(totals[index], `explorador.avaluo[${index}]`) == null ? null : Number(totals[index]) * 1_000_000_000,
    av_household: null,
    av_person: null,
    av_m2: null,
    households: nullableNumber(households[index], `explorador.hogares[${index}]`),
    urban_pct: nullableNumber(urban[index], `explorador.urbano[${index}]`)
  }));
}

async function fetchJson(url: string): Promise<unknown> {
  const response = await fetch(url, { cache: "force-cache" });
  if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
  return response.json() as Promise<unknown>;
}

export async function loadInsights(): Promise<InsightsLoadResult> {
  try {
    const data = parseInsightsV1(await fetchJson(INSIGHTS_URL));
    return { source: "v1", data, communes: data.communes, warning: null };
  } catch (primaryError) {
    try {
      const communes = parseLegacyCommunes(await fetchJson(LEGACY_COMMUNES_URL));
      const reason = primaryError instanceof Error ? primaryError.message : "artefacto v1 no disponible";
      return {
        source: "legacy",
        data: null,
        communes,
        warning: `Modo parcial: ${reason}. El gráfico comunal conserva sólo las métricas legacy verificables.`
      };
    } catch {
      throw primaryError;
    }
  }
}
