#!/usr/bin/env node
import { Agent } from '@strands-agents/sdk'
import { OpenAIModel } from '@strands-agents/sdk/models/openai'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = resolve(import.meta.dirname, '..')
const outPath = resolve(root, 'data/openai_agent_status.json')
const publicOutPath = resolve(root, 'public/data/openai_agent_status.json')

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
    // .env is optional; the shell environment is the normal source in Codex.
  }
}

function textFromMessage(message) {
  return (message?.content || [])
    .map((block) => {
      if (typeof block?.text === 'string') return block.text
      if (typeof block?.toJSON === 'function') return block.toJSON()?.text || ''
      return ''
    })
    .filter(Boolean)
    .join('\n')
    .trim()
}

function writeStatus(status) {
  const payload = {
    schema: 'aws-biopharma.openai-agent-status.v1',
    generated_at: new Date().toISOString(),
    ...status,
  }
  mkdirSync(resolve(root, 'data'), { recursive: true })
  mkdirSync(resolve(root, 'public/data'), { recursive: true })
  writeFileSync(outPath, `${JSON.stringify(payload, null, 2)}\n`)
  writeFileSync(publicOutPath, `${JSON.stringify(payload, null, 2)}\n`)
  console.log(JSON.stringify(payload, null, 2))
}

loadDotenv()

const apiKeyPresent = Boolean(process.env.OPENAI_API_KEY)
const modelId = process.env.OPENAI_MODEL || 'gpt-4o-mini'

if (!apiKeyPresent) {
  writeStatus({
    status: 'not_configured',
    provider: 'openai',
    model_id: modelId,
    api_key_present: false,
    note: 'OPENAI_API_KEY is not present in the shell environment or .env.',
  })
  process.exit(1)
}

try {
  const model = new OpenAIModel({
    api: 'chat',
    modelId,
    temperature: 0,
    maxTokens: 140,
  })
  const agent = new Agent({
    model,
    systemPrompt:
      'You are a concise AWS Biopharma hackathon assistant. Keep claims bounded to public-data evidence workflows, not clinical or treatment recommendations.',
  })
  const result = await agent.invoke(
    'In one sentence, state the role of OpenAI in this local AWS Biopharma demo.',
  )
  writeStatus({
    status: 'pass',
    provider: 'openai',
    model_id: modelId,
    api_key_present: true,
    stop_reason: result.stopReason,
    output: textFromMessage(result.lastMessage),
  })
} catch (error) {
  writeStatus({
    status: 'fail',
    provider: 'openai',
    model_id: modelId,
    api_key_present: true,
    error_type: error?.constructor?.name || 'Error',
    error: String(error?.message || error).slice(0, 500),
  })
  process.exit(1)
}

