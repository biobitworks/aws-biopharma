# Summary

This package governs the OpenAI-only red-team pass for the AWS Biopharma
dashboard.

Fastest safe next step:

```bash
npm run redteam:openai
npm run pull:data
npm run build:figures
npm run build:release
npm run verify:release
```

Approval required before execution:

- none for local OpenAI red-team status generation using the already supplied
  local API key
- explicit operator approval required before any live AWS, Convoke, Bright
  Data, KG, or provider writeback

Status:

- prompt package created
- implementation and verification pending
