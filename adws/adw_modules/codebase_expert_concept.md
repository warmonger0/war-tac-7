# Codebase-Expert Subagent: Context Optimization Pattern

## Overview

A specialized subagent that maintains comprehensive knowledge of the codebase structure and can intelligently recommend which files (and which parts of files) should be loaded for specific tasks.

## Architecture

### Phase 1: Codebase Indexing (One-time per project)

```python
# adws/adw_modules/codebase_indexer.py

def index_codebase(project_path: str) -> CodebaseIndex:
    """Create a lightweight index of the entire codebase.

    Returns:
        CodebaseIndex containing:
        - File paths and sizes
        - Function/class signatures (not full implementations)
        - Import dependencies
        - File relationships (what imports what)
        - Key sections per file (imports, classes, functions, exports)
    """
    index = {
        "files": {},
        "dependencies": {},
        "functions": {},
        "classes": {}
    }

    # Example index entry:
    # "app/server/core/llm_processor.py": {
    #     "size_lines": 250,
    #     "size_tokens": 4500,
    #     "imports": ["openai", "anthropic", "logging"],
    #     "exports": ["LLMProcessor"],
    #     "classes": {
    #         "LLMProcessor": {
    #             "lines": [20, 180],
    #             "methods": ["__init__", "generate_query", "validate_response"]
    #         }
    #     },
    #     "functions": {
    #         "parse_query": {"lines": [185, 220]}
    #     }
    # }

    return index
```

### Phase 2: Query Interface (Used by implementor)

```python
# adws/adw_modules/codebase_expert.py

class CodebaseExpertQuery:
    """Query the codebase expert for relevant files."""

    def get_relevant_files(
        self,
        task_description: str,
        codebase_index: CodebaseIndex
    ) -> FileLoadingStrategy:
        """
        Ask the codebase expert: "What should I load for this task?"

        Args:
            task_description: The plan/task from sdlc_planner
            codebase_index: The lightweight codebase index

        Returns:
            FileLoadingStrategy with:
            - must_read_full: Files that need complete loading
            - read_partial: Files where only sections are needed
            - read_signatures_only: Files where only signatures matter
            - skip: Files that can be ignored
        """

        # This would call a Claude Code subagent with:
        # - The task description
        # - The codebase index (lightweight!)
        # - Instructions to identify relevant files

        return FileLoadingStrategy(
            must_read_full=[
                "app/server/api/routes.py",  # Need to add new route
            ],
            read_partial={
                "app/server/core/llm_processor.py": {
                    "sections": ["class LLMProcessor", "generate_query function"],
                    "lines": [[20, 80], [120, 180]]
                }
            },
            read_signatures_only=[
                "app/server/core/db_manager.py",  # Just need to know interface
            ],
            skip=[
                "app/client/**",  # Not relevant to backend task
                "app/server/tests/**"  # Will write tests later
            ]
        )
```

### Phase 3: Implement in ADW Workflow

```python
# adws/adw_sdlc_ZTE_iso.py (modified)

def phase_implement(adw_id: str, plan_path: str):
    """Implementation phase with codebase-expert optimization."""

    # Step 1: Load the plan (lightweight)
    with open(plan_path) as f:
        plan_content = f.read()

    # Step 2: Query codebase expert (NEW!)
    codebase_index = load_codebase_index(get_project_root())

    expert_query = CodebaseExpertQuery()
    loading_strategy = expert_query.get_relevant_files(
        task_description=plan_content,
        codebase_index=codebase_index
    )

    # Step 3: Create focused context instruction (NEW!)
    context_instruction = f"""
## Context Loading Strategy (Pre-Computed)

Based on analysis of your task, you should:

**Load Full Files:**
{chr(10).join(f'- {f}' for f in loading_strategy.must_read_full)}

**Load Partial Files:**
{chr(10).join(
    f'- {f}: lines {ranges}'
    for f, info in loading_strategy.read_partial.items()
    for ranges in info['lines']
)}

**Signatures Only (for reference):**
{chr(10).join(f'- {f}' for f in loading_strategy.read_signatures_only)}

**Skip These (not relevant):**
{chr(10).join(f'- {f}' for f in loading_strategy.skip)}

This strategy was pre-computed to minimize context loading.
Follow it to stay within context budget.
"""

    # Step 4: Call implementor with focused instructions
    implement_request = AgentTemplateRequest(
        agent_name="sdlc_implementor",
        slash_command="/implement",
        args=[context_instruction + "\n\n" + plan_content],
        adw_id=adw_id,
        working_dir=get_worktree_path(adw_id)
    )

    response = execute_template(implement_request)
    return response
```

## Slash Command: /query_codebase_expert

```markdown
# Query Codebase Expert

Ask the codebase expert which files are relevant for a task.

## Variables
task_description: $1
codebase_index_path: $2 (optional, defaults to .codebase_index.json)

## Instructions

You are the codebase expert. Your job is to analyze a task and recommend which files should be loaded.

You have access to a lightweight codebase index (provided below) that contains:
- File paths and sizes
- Function/class signatures
- Import dependencies
- File relationships

**Your goal**: Minimize context loading while ensuring the implementor has everything needed.

## Codebase Index
$CODEBASE_INDEX

## Task Description
$TASK_DESCRIPTION

## Output Format

Return a JSON object with this structure:

```json
{
  "must_read_full": [
    {
      "path": "app/server/api/routes.py",
      "reason": "Need to add new endpoint, requires full context"
    }
  ],
  "read_partial": [
    {
      "path": "app/server/core/llm_processor.py",
      "sections": [
        {
          "name": "LLMProcessor class",
          "lines": [20, 180],
          "reason": "Need to understand the interface"
        }
      ]
    }
  ],
  "read_signatures_only": [
    {
      "path": "app/server/core/db_manager.py",
      "reason": "Just need to know the API, not implementation"
    }
  ],
  "skip": [
    {
      "pattern": "app/client/**",
      "reason": "Backend-only task, no UI changes"
    }
  ],
  "estimated_tokens": 15000,
  "reasoning": "Brief explanation of your recommendations"
}
```

## Guidelines

1. **Be Conservative**: If unsure, include the file
2. **Prefer Partial Reads**: If only specific functions are relevant, specify line ranges
3. **Consider Dependencies**: If A imports B, might need B's signatures
4. **Skip Tests Initially**: Tests can be read when writing new tests
5. **Minimize Frontend/Backend Crossing**: If backend task, skip frontend files
```

## Benefits

### Context Reduction
- **Current**: sdlc_implementor loads 50-70K tokens of codebase context
- **With Expert**: Loads only 10-20K tokens of relevant context
- **Savings**: 60-70% reduction in context size

### Cache Efficiency
- **Current**: 85-90% efficiency during warmup
- **With Expert**: 95-98% efficiency from start
- **Why**: Smaller, more focused context = better cache reuse

### Cost Savings
- **Per workflow**: $2-4 saved on implementor phase
- **Across 10 issues/month**: $20-40 saved
- **Plus**: Faster execution (fewer tokens = faster responses)

## Implementation Phases

### Phase 1: Manual (Immediate)
- Create codebase index manually
- Add "Context Loading Strategy" to plan template
- Human reviews and approves file list

### Phase 2: Semi-Automated (1-2 weeks)
- Build codebase indexer script
- Create /query_codebase_expert slash command
- Planner calls expert, includes recommendations in plan

### Phase 3: Fully Automated (1 month)
- Integrate into ADW workflow automatically
- Expert runs before implementor
- Context strategy passed to implementor
- Monitoring and metrics on context savings

## Example Workflow

```bash
# 1. Index codebase (one-time)
uv run adws/index_codebase.py projects/tac-webbuilder > .codebase_index.json

# 2. Planner creates plan as usual
/feature "Add user authentication"

# 3. Before implementing, query expert
/query_codebase_expert "$(cat specs/issue-X-plan.md)" .codebase_index.json

# 4. Expert returns focused file list (JSON)

# 5. Implementor receives plan + context strategy
/implement "
## Context Strategy (from expert)
Load: app/server/auth/*.py (full)
Load: app/server/api/routes.py lines 1-50, 200-250 (partial)
Skip: app/client/** (not relevant)

## Plan
[original plan]
"

# 6. Implementor loads minimal context and implements
```

## Metrics to Track

After implementation, track:
- Context size before/after expert consultation
- Cache efficiency improvement
- Cost savings per workflow
- Time savings per workflow
- Quality of recommendations (did implementor need additional files?)

## Next Steps

1. **Prototype**: Create simple codebase indexer
2. **Test**: Manually create context strategy for Issue 8a
3. **Compare**: Run 8a with/without expert recommendation
4. **Measure**: Track context size, cost, and quality
5. **Iterate**: Refine expert prompts based on results
6. **Automate**: Integrate into ADW workflow
