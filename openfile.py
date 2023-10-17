import csv
from re import sub



def openfile():
    """
    открываем файл, создаем список, возвращаем его
    """
    with open('homeworkregexp/phonebook_raw.csv') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def correctionname():
    """ 
    перебираем файл, объединяем 3 первых элемента списка, после разделяем его
    добавляем данные в новый список и после добавляем в общий список
    """
    new_contacts_list = []
    for columns in openfile():
        contact = []
        name = " ".join(columns[0:3])
        name = name.split(" ",2)
        for columnsname in name:
            columnsname = columnsname.strip()
            contact.append(columnsname)
        for columnsname2 in columns[3:7]:
            contact.append(columnsname2)
        new_contacts_list.append(contact)
    return new_contacts_list


def correctionphone():
    """
    перебираем все элементы списка списков, проверяем на наличие патерна, если есть то заменяем его
    после добавлем данные в список
    """
    new_contacts_list = []
    for name in correctionname():
        add_info = []
        for columns in name:
            pattern = r"(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\-*(\d{2})\-*(\d{2})((\s*)\s*\(*(доб\.*)\s*(\d{4})\)*)?"
            result = sub(pattern, r"+7(\2)\3-\4-\5\7\8\9", columns)
            columns = result
            add_info.append(columns)
        new_contacts_list.append(add_info)
    return new_contacts_list


def duplicates():
    """
    в цикле проверяем на равенство Фамилии и Имени, и заменяем переменные
    После добавляем значения в новый список если их нет в нём
    """
    last_list = []
    new_contacts_list = correctionphone()
    for l in new_contacts_list[1:]:
        for j in new_contacts_list[1:]:
            if l[0] == j[0] and l[1] == j[1]:
                if l[2] == '':
                    l[2] = j[2]
                if l[3] == '':
                    l[3] = j[3]
                if l[4] == '':
                    l[4] = j[4]
                if l[5] == '':
                    l[5] = j[5]
                if l[6] == '':
                    l[6] = j[6]
    for columns in new_contacts_list:
        if columns not in last_list:
            last_list.append(columns)          
    return last_list


def createcsv():
    """
    создаём новый csv и добавляем в него наш список
    """
    with open("homeworkregexp/phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(duplicates())