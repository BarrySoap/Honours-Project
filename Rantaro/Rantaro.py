_name = "Glenn"

print(6**3)     # Exponentials
print(9//4)     # Forced Integer Division
print(9 % 6)    # Modulo

string_one = 'Sentence "One"'
string_two = "Sentence 'Two'"
string_three = '    Sentence \'Three\'  '
string_four = '''Sentence
Four
Is
Longer'''

print(string_one.upper())
print(string_two.title())
print(string_three.strip().upper())

astr = string_one + string_two
astr = astr.replace("\"One\"", "Three ")
astr = astr.replace("Sentence", "Sent")
print(astr)