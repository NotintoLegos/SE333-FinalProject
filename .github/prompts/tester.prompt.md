---
mode: "agent"
tools: [analyze_java_file, generate_junit_test, execute_tests, parse_jacoco_report, get_coverage_recommendations, git_status, git_add_all, git_commit, git_push, git_pull_request]
description: "AI testing agent that generates tests, improves coverage, and manages git operations"
model: 'Gpt-5 mini'
---

## Follow Instructions below: ##
1. first find all the source code to test
2. generate test
3. run test using 'mvn test'
4. if test has errors, fix it and run 'mvn test'
5. find coverage using 'jacoco_find_path'
6. then use the path and parse it using 'missing_coverage'
7. if there is missing coverage, generate more tests to cover it
8. repeat steps 3-7 until 'jacoco_coverage' shows 100% coverage or 'missing_coverage' shows zero