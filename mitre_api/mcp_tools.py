from fastmcp import FastMCP, Context

mcp = FastMCP("MITRE ATTACK Framework Reasoner")


@mcp.tool()
def map_attack_to_control(technique_ids: list[str], control_statement: str) -> str:
    """
    First-pass mapping from MITRE technique to whether/how the control statement provides visibility or mitigation.
    """
    return f"""
You are a cybersecurity analyst.

Evaluate whether the control statement below provides visibility or mitigation against this MITRE ATT&CK technique.

List of Technique IDs: {technique_ids}
Control: {control_statement}

List reasoning and expected observable artifacts if applicable.
"""


@mcp.tool()
def reflect_mapping_rationale(original_reasoning: str) -> str:
    """
    Asks the LLM to self-criticize and refine its reasoning: did it miss anything? Are assumptions valid?
    """
    return f"""
You are now acting as a self-reflective cybersecurity expert.

Review this reasoning output from another analyst mapping a MITRE technique to a control statement.

Does the mapping make strong assumptions? Are there edge cases where the control fails to detect the behavior? What supporting evidence or counterexamples would strengthen the claim?

Original Mapping Reasoning:
---
{original_reasoning}
---

Write an improved or more cautious analysis.
"""


@mcp.tool()
def grade_mapping_confidence(reasoning: str) -> str:
    """
    Grades the confidence level (High, Medium, Low) of the MITRE-to-control mapping based on the reasoning quality.
    Flags weak assumptions and suggests improvements.
    """
    return f"""
You are a cybersecurity expert evaluating reasoning quality.

Below is an explanation mapping a MITRE ATT&CK technique to a defensive control. Your task is to assess the **confidence level** of this mapping:

- High: Strong justification, observable evidence clearly supports the control's coverage of the technique.
- Medium: Partially valid, but some assumptions or gaps exist.
- Low: Weak reasoning or unrealistic assumptions; control likely does not cover the technique reliably.

Also point out:
- Any assumptions made
- Missing telemetry/log sources
- Suggestions to improve the mapping

### Reasoning:
{reasoning}

### Your Assessment:
Confidence Level:
Assumptions:
Gaps or Weaknesses:
Suggestions for Improvement:
"""


#! This doesn't really work to orchestrate the loop. But can be used as part of the MCP client to call the tools in sequence.
@mcp.tool()
def analyze_until_confident(previous_reasoning: str) -> str:
    """
    Review the provided mapping reasoning and decide if it is sufficiently confident.
    If confidence is not 'High', revise and retry up to 2 more times.
    Output the final result in JSON.
    """
    return f"""
You are a cybersecurity reasoning engine with self-reflective capabilities.

Below is a previous attempt to map a MITRE ATT&CK technique to a control statement.

You must assess:
- Whether the reasoning is complete, cautious, and logically sound
- If confidence is not **High**, improve the reasoning and try again (up to 3 total attempts)

Stop once the explanation reaches **High confidence**, or after 3 iterations.

Return the final result in this JSON format:
{{
  "final_iteration": 1,
  "confidence_level": "High | Medium | Low",
  "refined_reasoning": "...",
  "assumptions": "...",
  "gaps_or_weaknesses": "...",
  "suggestions_for_improvement": "..."
}}

### Previous Reasoning:
{previous_reasoning}

Begin self-reflection.
"""


if __name__ == "__main__":
    mcp.run(transport="http", port=1234)
