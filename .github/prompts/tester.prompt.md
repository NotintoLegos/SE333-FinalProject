---
mode: "agent"
tools: ["find_jacoco_patt", "missing_coverage"]
description: "description of the tool`
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
8. repeat steps 3-7 until 'jacoco_coverage' shows 100% coverage or 'misssing_coverage' shows is zero