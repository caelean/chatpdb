from typing import List, Dict

shared_context_template = """
## Context
<stacktrace>
{stack_trace}
</stacktrace>
<code>
{source_code}
</code>
<frame_variables>
<locals>
{locals}
</locals>
<globals>
{globals}
</globals>
</frame_variables>
"""

template = (
    shared_context_template
    + """
## Instructions
The context information comes from a currently running Python debugger session.
Use this information to explain the current state of the program, focusing specifically on the
 most relevant pieces of code, variable state, or the stack trace.
Your response must:
- be clear and concise
- focus on the most relevant information, particularly any errors, issues, or recent state changes
- make minimal assumptions about external code or context
"""
)

exception_template = (
    shared_context_template
    + """
<exception>
{exception}
</exception>

## Instructions
The context information comes from a currently running Python debugger session.
The context includes an exception that was just raised.
Explain why the exception occurred and how it relates to the current state of the program.

Your response must:
- be clear and concise
- focus on the most relevant information
- make minimal assumptions about external code or context
"""
)


def get_explain_prompt(
    stack_trace: List[str],
    source_code: str,
    local_vars: Dict[str, str],
    global_vars: Dict[str, str],
    exception: str = "",
) -> str:
    if exception:
        return exception_template.format(
            stack_trace="\n".join(stack_trace),
            source_code=source_code,
            locals="\n".join(f"{k}: {v}" for k, v in local_vars.items()),
            globals="\n".join(f"{k}: {v}" for k, v in global_vars.items()),
            exception=exception,
        )
    return template.format(
        stack_trace="\n".join(stack_trace),
        source_code=source_code,
        locals="\n".join(f"{k}: {v}" for k, v in local_vars.items()),
        globals="\n".join(f"{k}: {v}" for k, v in global_vars.items()),
    )
