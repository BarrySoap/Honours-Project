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

first_name = str(input("Enter your first name: "))
middle_name = str(input("Enter your middle name: "))
last_name = str(input("Enter your last name: "))

first_name = first_name.capitalize()
middle_name = middle_name.capitalize()
last_name = last_name.capitalize()

name_format = "{first} {middle:.1s} {last}"
print(name_format.format(first=first_name, middle = middle_name, last = last_name))

sentences = [string_one, string_two, string_three, string_four]

alpha = ["a", "b", "c", "d"]
alpha.append("e")
alpha = alpha + ["f", "g"]
d_index = alpha.index("d")
del alpha[d_index]
alpha.remove("f")