# Corporate Boundary Axiom + Plugin Provider Architecture

**Date:** 2026-03-04
**Status:** Approved
**Repos affected:** `obsidian-hapax`, `hapaxromana`, `hapax-system`

## Problem

The Obsidian plugin (`obsidian-hapax`) currently requires localhost services (LiteLLM :4000, Qdrant :6333, Ollama :11434) for all functionality. On the isolated institutional compartment device (behind strict egress proxy), these services are unreachable. The plugin must support direct calls to compartment-sanctioned LLM providers (OpenAI, Anthropic) to be usable at work.

The Obsidian vault syncs across all devices via approved compartment git transport. This is the only acceptable data transport across the corporate boundary.

## Axiom: corporate_boundary (weight: 90)

The Obsidian plugin operates across a corporate network boundary across an institutional compartment boundary. When running on external institutional compartment devices, all external API calls must use compartment-sanctioned providers (currently: OpenAI, Anthropic). No localhost service dependencies may be assumed. The system must degrade gracefully when home-only services (Qdrant, Ollama, LiteLLM, health monitor) are unreachable.

### T0 Blocking Implications

| ID | Description |
|---|---|
| `cb-llm-001` | Plugin must support direct API calls to sanctioned providers (OpenAI, Anthropic) without requiring a localhost proxy |
| `cb-data-001` | Obsidian <-> hapax data flow must use only approved compartment git transport. Plugin must never require direct network access to home services for core functionality |
| `cb-degrade-001` | Features depending on localhost services (RAG search, health status, embedding) must fail silently with informative UI, not throw errors |
| `cb-key-001` | API credentials in plugin settings are acceptable (compartment settings remain strictly local). No secrets may be stored outside the plugin's data.json |

## Architecture: Provider Abstraction Layer

### LLMProvider Interface

```typescript
interface LLMProvider {
  streamChat(
    messages: Array<{ role: string; content: string }>,
    model: string,
    signal?: AbortSignal
  ): AsyncGenerator<string, void, unknown>;
}
```

### Implementations

**OpenAICompatibleProvider** — handles LiteLLM and direct OpenAI. Same SSE format (`data: {"choices":[{"delta":{"content":"..."}}]}`). Constructor takes `baseUrl` + `apiKey`.

**AnthropicProvider** — handles Anthropic Messages API. Different SSE format (`event: content_block_delta`, `data: {"delta":{"type":"text_delta","text":"..."}}`). Requires `x-api-key` header + `anthropic-version` header. Constructor takes `apiKey`.

### Settings

New `provider` field: `"litellm"` (default) | `"openai"` | `"anthropic"`

Settings UI adapts per provider:
- **litellm:** LiteLLM URL + API key + full model dropdown (all aliases)
- **openai:** API key + OpenAI model dropdown
- **anthropic:** API key + Anthropic model dropdown

Model dropdowns:
- **LiteLLM:** claude-sonnet, claude-haiku, claude-opus, gemini-pro, gemini-flash, qwen-coder-32b, qwen-7b
- **OpenAI:** gpt-4o, gpt-4o-mini, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, o3, o4-mini
- **Anthropic:** claude-sonnet-4-6, claude-opus-4-6, claude-haiku-4-5-20251001

### Graceful Degradation

| Feature | Home (localhost available) | Work (no localhost) |
|---|---|---|
| Chat | Via LiteLLM proxy | Direct OpenAI/Anthropic |
| Knowledge search | Qdrant + Ollama embeddings | Notice: "Requires home network" |
| Prepare 1:1 | Vault data + Qdrant RAG | Vault data only (RAG skipped silently) |
| Team snapshot | Vault data + Qdrant RAG | Vault data only (RAG skipped silently) |
| Status bar | Health history file | Shows "Hapax: ?" (already works) |
| Nudges | Opens vault file | Works (vault-only) |

## Extensibility Plan

Adding a new provider requires:
1. Implement `LLMProvider` interface (~30-50 lines)
2. Add entry to provider dropdown in settings.ts
3. Add model list for the provider
4. Update `createProvider()` factory

Planned future providers:
- `google` — Gemini API
- `azure-openai` — Azure-hosted OpenAI (different base URL + auth)
- `custom` — user-supplied OpenAI-compatible endpoint (covers corporate gateways)

## File Changes

| File | Change |
|---|---|
| `src/types.ts` | Add `provider` field to HapaxSettings, add LLMProvider interface |
| `src/providers/openai-compatible.ts` | New — OpenAICompatibleProvider |
| `src/providers/anthropic.ts` | New — AnthropicProvider with Messages API streaming |
| `src/providers/index.ts` | New — createProvider() factory |
| `src/llm-client.ts` | Refactor to delegate to provider |
| `src/settings.ts` | Provider dropdown, conditional fields, per-provider model lists |
| `src/commands/search.ts` | Better UX when Qdrant unreachable |
| `hapaxromana/axioms/` | New corporate_boundary axiom |
| `hapax-system/rules/axioms.md` | Add axiom + T0 implications |

## Context

- Work device: isolated institutional compartment client behind egress proxy
- Direct HTTPS to api.anthropic.com and api.openai.com works through institutional egress proxy
- API keys in plugin settings acceptable (compartment settings remain strictly local)
- Only the work device has the "sanctioned providers only" constraint
- Home devices + rest of hapax system: unrestricted
