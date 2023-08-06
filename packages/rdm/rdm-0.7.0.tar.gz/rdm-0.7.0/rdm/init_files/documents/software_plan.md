{% extends "base/software_plan.md" %}

{% block project_details %}
## Development Standards

TODO: The project lead should keep an up-to-date list of development standards here (e.g., PEP8 on a Python project).

If the software system's safety classification is not level C (the highest), you may delete this section.

[[:This section fulfills 5.1.4.a]]

## Development Methods

TODO: The project lead should keep an up-to-date list of development methods here (e.g., Test Driven Development) if relevant.

If the software system's safety classification is not level C (the highest), you may delete this section.

[[:This section fulfills 5.1.4.b]]

## Development Tools

TODO: The project lead should keep an up-to-date list of development tools here, such as linters and versions.

If the software system's safety classification is not level C (the highest), you may delete this section.

To the extent possible, checking against these standards should be performed in an automated fashion (e.g., using a linter which is run on a git-commit hook) [[:5.1.4]].

[[:This section fulfills 5.1.4.c]]

## Testing Plan

TODO: Write out a testing plan for {{ system.project_name }}.

This plan should include a pass/fail criteria for the entire test suite.  E.g., you require that all unit tests pass and that all integration tests pass or the cause of the failure is understood and justified [[62304:5.7.1.a]]

[[62304:5.5.2]]

{% endblock %}

{% block software_archival_task %}
TODO: Write out the task that should be followed in order to archive the software system release.  This will vary from project to project.  Here are some exmples:

- If the output of the build process is a binary, then the binary should be saved somewhere.
- If the output is a set of Python scripts with out any SOUP, then the source code within the git repo is already sufficient.
- If the output is a set of Python scripts with Python dependencies, then copies of the Python dependencies must be archived somewhere.  Likewise, if there are other system dependencies, like postgres, then the debian package files (or perhaps a virtual box image) need to be archived.

The purpose of the archive is to provide a means to re-test problems which may occur in an old version of the software.

{% endblock %}
