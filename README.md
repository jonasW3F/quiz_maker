# Quiz Maker

This script generates two exams from all the `q{number}.tex` in the folder. These questions need to be formatted as in the two example questions. We can also add a `[correct]` indication in front of the answer to mark which answer is correct.

The script does the following:
1) It creates two exams by randomizing the order of the questions **and** the order of the answers.
2) It creates two solution files that include the [correct] tag per question, so it is easier to track where the correct answers are.
