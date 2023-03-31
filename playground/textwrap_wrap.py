"""
https://stackoverflow.com/a/74242080
"""
import textwrap

text = "Here the line that have to be under 120 chars and cut at the point in the string where the last word is under 120 chars because this part have to be in the second line and it also needs to be seperated such as the string part before and this has to be in the third line with the end of the string"
print(*textwrap.wrap(text, 10), sep='\n')