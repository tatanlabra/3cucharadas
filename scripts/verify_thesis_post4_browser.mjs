#!/usr/bin/env node
import { main } from './verify_thesis_series_browser.mjs';

try {
  await main(4);
} catch (error) {
  console.error(JSON.stringify({ status: 'ERROR', error: error.message }));
  process.exitCode = 2;
}
