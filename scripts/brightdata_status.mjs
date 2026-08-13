#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = resolve(import.meta.dirname, '..')
const outPath = resolve(root, 'data/brightdata_status.json')
const publicOutPath = resolve(root, 'public/data/brightdata_status.json')
const tokenNames = [
  'BRIGHTDATA_API_KEY',
  'BRIGHT_DATA_API_KEY',
  'BRIGHTDATA_TOKEN',
  'BRIGHT_DATA_TOKEN',
]

function loadDotenv() {
  try {
    const text = readFileSync(resolve(root, '.env'), 'utf8')
    for (const rawLine of text.split(/\r?\n/)) {
      const line = rawLine.trim()
      if (!line || line.startsWith('#') || !line.includes('=')) continue
      const [key, ...rest] = line.split('=')
      if (!process.env[key]) {
        process.env[key] = rest.join('=').trim().replace(/^['"]|['"]$/g, '')
      }
    }
  } catch {
    // .env is optional; never write provider secrets from this script.
  }
}

function firstToken() {
  for (const name of tokenNames) {
    const value = process.env[name]
    if (value && !['...', 'changeme', 'paste_key_here', 'paste_token_here'].includes(value.toLowerCase())) {
      return true
    }
  }
  return false
}

function packageVersion() {
  try {
    const pkg = JSON.parse(readFileSync(resolve(root, 'node_modules/@brightdata/mcp/package.json'), 'utf8'))
    return pkg.version || null
  } catch {
    return null
  }
}

loadDotenv()

const token = firstToken()
const payload = {
  schema: 'aws-biopharma.brightdata-status.v1',
  generated_at: new Date().toISOString(),
  provider: 'brightdata',
  status: token ? 'configured' : 'token_not_visible',
  package: '@brightdata/mcp',
  package_version: packageVersion(),
  mcp_server: 'bright-data',
  credential_status: token ? 'configured locally; value not published' : 'optional; not visible',
  groups: process.env.BRIGHTDATA_GROUPS || 'code',
  note: token
    ? 'Bright Data MCP can be started locally from .mcp.json. This status check does not spend credits or call Bright Data APIs.'
    : 'Bright Data MCP is configured, but no token alias is visible in this shell or .env.',
}

mkdirSync(resolve(root, 'data'), { recursive: true })
mkdirSync(resolve(root, 'public/data'), { recursive: true })
writeFileSync(outPath, `${JSON.stringify(payload, null, 2)}\n`)
writeFileSync(publicOutPath, `${JSON.stringify(payload, null, 2)}\n`)
console.log(JSON.stringify(payload, null, 2))
