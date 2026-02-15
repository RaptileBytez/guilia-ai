# 📚 Prompt Research & Library Notes

## Source: DataCamp Associate AI Engineer
This directory serves as a curated reference library for various Prompt Engineering techniques. The prompts originated primarily from the DataCamp course and are optimized for general LLM stability and specific OpenAI behaviors.

## Observations & Research
- **Language Drifting:** In long-turn conversations, the model tends to drift back into the language of the System Prompt (English). *Current Mitigation: Added a Language Protocol to core instructions.*
- **Model Specifics:** OpenAI-optimized prompts (found in `openai_optimized`) frequently utilize the `Instruction -> Context -> Task` structure. 
- **Adaptation Note:** These may require structural re-ordering (Task-at-end) when ported to Llama-based models or specific local deployments.

## Organization
- **Analysis:** Classification logic and entity extraction templates.
- **Coding:** Diverse tools for code explanation, generation, and modification.
- **Transformation:** Prompts for summarization, proofreading, and tone adjustment.

## Future Tasks & Roadmap
- [ ] **Code-Review Integration:** Implementation of a specialized summarizer for PR/Code reviews.
- [ ] **Model Benchmarking:** Test classification prompts with Gemini 1.5 Flash vs. Pro to evaluate reasoning depth vs. speed.
- [ ] **Task Mapping:** Automate the selection of these library prompts based on user intent detection.