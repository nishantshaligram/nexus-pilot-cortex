# Supported Models & Pricing Reference

NexusPilot Cortex calculates operational costs dynamically based on model pricing tables (USD per 1M tokens).

---

## Default Pricing Table

| Model ID | Input Tokens ($ / 1M) | Cached Input ($ / 1M) | Output Tokens ($ / 1M) | Cache Discount |
| :--- | :--- | :--- | :--- | :--- |
| **`gemini-2.0-flash`** | \$0.10 | \$0.025 | \$0.40 | 75% |
| **`gemini-1.5-flash`** | \$0.075 | \$0.01875 | \$0.30 | 75% |
| **`gemini-1.5-pro`** | \$1.25 | \$0.3125 | \$5.00 | 75% |
| **`claude-3-5-sonnet`**| \$3.00 | \$0.30 | \$15.00 | 90% |
| **`gpt-4o`** | \$2.50 | \$1.25 | \$10.00 | 50% |
| **`default`** | \$0.10 | \$0.025 | \$0.40 | 75% |

---

## Prefix Caching ROI

With Gemini and Claude models, prompt cache hits yield up to a **75% to 90% cost reduction** and significantly reduced Time-to-First-Token (TTFT). Cortex actively monitors this ratio on every turn.
