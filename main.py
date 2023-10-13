import csv
import re


with open("phonebook_raw.csv", encoding="utf-8", newline='') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

temp_contact_list = []

pattern = re.compile(r"(\+7|8)\s*\(?(\d{3})\)?\s*-?(\d{3})-?(\d{2})-?(\d{2})\s?(\(?(доб.)\s*(\d+)\)?)?")

"""
В коде c 22й по 38ю строки редактирую и пересобираю каждый контакт.
 - ФИО через .join с последующим разбитием через split(). Если контакт не имеет отчества, то добавляют пробел,
   для сохранения общей длинны строки в 7 элементов.
 - Номер телефона редактирую через регулярное выражение, а при его отсутствии вставляю пробел
 - В конце добавляю к каждому контакту адрес электронной почты - элемент с индексом 6
 Пересобранные контакты храню в temp_contact_list
"""

for elem in contacts_list[1:]:
    fixed_contact = []
    joined_name = ' '.join(elem[0:3])

    if len(joined_name.split()) == 2:
        fixed_contact.extend(joined_name.split())
        fixed_contact.extend(" ")
    else:
        fixed_contact.extend(joined_name.split())
    fixed_contact.extend(elem[3:5])
    if elem[5]:
        fixed_phone = pattern.sub(r"+7(\2)\3-\4-\5 \7\8", elem[5])
        fixed_contact.append(fixed_phone.strip())
    else:
        fixed_contact.append(' ')
    fixed_contact.append(elem[6])
    temp_contact_list.append(fixed_contact)

temp_contact_list.sort(key=lambda x: x[0])

final_contact_list = []
final_contact_list.append(contacts_list[0])
index_list = []

"""
В коде c 54й по 72ю в отсортированном списке temp_contact_list (в алфавитном порядке по фамилии)
ищу контакты, у которых совпадет имя и фамилия. Отдельно сохраняю их индексы в index_list, т.к. далее на их основе 
в строке 70 создам еще один список уникальных контактов - remaining_contact. 
Две пары совпадающих контактов объединяю через zip и конечный вариант записываю в список final_contact_list.
В конце остаётся соединить списки final_contact_list и temp_contact_list, отсортировать и записать в файл
"""

for i in range(len(temp_contact_list)-1):
    if temp_contact_list[i][:2] == temp_contact_list[i + 1][:2]:
        index_list.append(i)
        index_list.append(i+1)

        temp_list = []
        zipped = zip(temp_contact_list[i], temp_contact_list[i + 1])
        for pair in zipped:
            if pair[0]:
                temp_list.append(pair[0])
            elif pair[1]:
                temp_list.append(pair[1])
            elif not pair[0] and not pair[1]:
                temp_list.append(' ')
        final_contact_list.append(temp_list)

remaining_contact = [value for id, value in enumerate(temp_contact_list) if id not in index_list]
final_contact_list.extend(remaining_contact)
final_contact_list.sort(key=lambda x: x[0])

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contact_list)
    