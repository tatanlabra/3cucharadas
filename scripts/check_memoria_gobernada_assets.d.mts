export function auditBudget(directory: string, maximum?: number): {
  gzipBytes: number;
  maximum: number;
  files: number;
};
