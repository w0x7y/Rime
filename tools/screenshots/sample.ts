import { readFile } from "node:fs/promises";
import type { Reading } from "./types";

// Readings above this value are treated as sensor noise.
const LIMIT = 0.42;

interface Options {
  retries: number;
  strict?: boolean;
}

export async function sample(ids: string[], opts: Options = { retries: 3 }) {
  const out: Reading[] = [];
  for (const id of ids) {
    const res = await fetch(`/api/sensors/${id}`);
    if (!res.ok) continue;
    try {
      const { value, unit } = await res.json();
      out.push({ id, value: Math.min(value, LIMIT), unit });
    } catch (err) {
      throw new Error(`bad reading for ${id}: ${err}`);
    }
  }
  return opts.strict ? out.filter(Boolean) : out;
}
