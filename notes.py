from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QListWidget, QPushButton, QLineEdit, QInputDialog, QMessageBox
import json

app = QApplication([])

window = QWidget()
window.resize(630,585)
window.setWindowTitle('Розумні замітки')

content = QTextEdit(window)
content.resize(290,570)
content.move(10,10)
content.hide()
content.setPlaceholderText('Почніть писати ваші нотатки тут')

title_note_list = QLabel(window)
title_note_list.move(305, 10)
title_note_list.setText('Список заміток')

notes_list = QListWidget(window)
notes_list.resize(320, 190)
notes_list.move(305,30)

create_btn = QPushButton(window)
create_btn.resize(170,30)
create_btn.move(300, 225)
create_btn.setText('Створити замітку')
create_btn.setShortcut('Ctrl+N')

delete_btn = QPushButton(window)
delete_btn.resize(170,30)
delete_btn.move(465, 225)
delete_btn.setText('Видалити замітку')
delete_btn.setShortcut('Ctrl+D')

save_btn = QPushButton(window)
save_btn.resize(335,30)
save_btn.move(300, 250)
save_btn.setText('Зберегти замітку')
save_btn.setShortcut('Ctrl+S')

title_tag_list = QLabel(window)
title_tag_list.move(305, 280)
title_tag_list.setText('Список тегів')

tags_list = QListWidget(window)
tags_list.resize(320, 190)
tags_list.move(305,300)

write_tag_line = QLineEdit(window)
write_tag_line.resize(320,30)
write_tag_line.move(305, 495)
write_tag_line.setPlaceholderText('Введіть тег...')

add_tag_btn = QPushButton(window)
add_tag_btn.resize(170,30)
add_tag_btn.move(300, 525)
add_tag_btn.setText('Додати до замітки')
add_tag_btn.setShortcut('Ctrl+G')

delete_tag_btn = QPushButton(window)
delete_tag_btn.resize(170,30)
delete_tag_btn.move(465, 525)
delete_tag_btn.setText('Відкріпити від замітки')
delete_tag_btn.setShortcut('Ctrl+U')

search_tag_btn = QPushButton(window)
search_tag_btn.resize(335,30)
search_tag_btn.move(300, 550)
search_tag_btn.setText('Шукати замітки по тегу')
search_tag_btn.setShortcut('Ctrl+F')

my_note_dict = {}
with open('main.json', 'r') as file:
    my_note_dict = json.load(file)

notes_list.addItems(my_note_dict)

def check(item):
    global note_name
    note_name = item
    content.clear()
    content.setText(my_note_dict[note_name.text()]['text'])
    content.show()
    tags_list.clear()
    tags_list.addItems(my_note_dict[note_name.text()]['tags'])
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def create_note():
    global text
    text, ok = QInputDialog.getText(window, 'Створити замітку', 'Назва замітки:')
    if ok and text == '':
        not_creating = QMessageBox()
        not_creating.setText('Ви не ввели назву!')
        not_creating.exec_()
    elif ok and text != '':
        my_note_dict[text] = {'text' : '', 'tags' : []}
        notes_list.clear()
        notes_list.addItems(my_note_dict)
        tags_list.clear()
        content.hide()
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def delete_note():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        my_note_dict.pop(note)
        note_num = notes_list.indexFromItem(note_name).row()
        notes_list.takeItem(note_num)
        tags_list.clear()
        content.clear()
        content.hide()
    else:
        not_deleting = QMessageBox()
        not_deleting.setText('Замітка не обрана!')
        not_deleting.exec_()
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def save_note():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        note_text = content.toPlainText()
        my_note_dict[note]['text'] = note_text
        saved_msg_box = QMessageBox()
        saved_msg_box.setText('Замітка успішно збережена!')
        saved_msg_box.exec_()
    else:
        not_saving = QMessageBox()
        not_saving.setText('Замітка не знайдена!')
        not_saving.exec_()
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = write_tag_line.text()
        if not tag in my_note_dict[key]['tags']:
            my_note_dict[key]['tags'].append(tag)
            tags_list.addItem(tag)
            write_tag_line.clear()
    else:
        write_tag_line.clear()
        not_added = QMessageBox()
        not_added.setText('Замітка не обрана!')
        not_added.exec_()
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def delete_tag():
    if tags_list.selectedItems():
        tag = tags_list.selectedItems()[0]
        tag_num = tags_list.indexFromItem(tag).row()
        tags_list.takeItem(tag_num)
        my_note_dict[note_name.text()]['tags'].pop(tag_num)
    else:
        write_tag_line.clear()
        not_deleting_tag = QMessageBox()
        not_deleting_tag.setText('Тег не обран!')
        not_deleting_tag.exec_()
    with open('main.json', 'w') as file:
        json.dump(my_note_dict, file)
def search_tag():
    tag_text = write_tag_line.text()
    if search_tag_btn.text() == 'Шукати замітки по тегу' and tag_text:
        filtered_notes = {}
        for note in my_note_dict:
            if tag_text in my_note_dict[note]['tags']:
                filtered_notes[note] = my_note_dict[note]
        search_tag_btn.setText('Скинути пошук')
        content.hide()
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(filtered_notes)
    elif search_tag_btn.text() == 'Скинути пошук':
        content.hide()
        write_tag_line.clear()
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(my_note_dict)
        search_tag_btn.setText('Шукати замітки по тегу')
    else:
        not_searched = QMessageBox()
        not_searched.setText('Ви не ввели тег!')
        not_searched.exec_()

notes_list.itemClicked.connect(check)
create_btn.clicked.connect(create_note)
delete_btn.clicked.connect(delete_note)
save_btn.clicked.connect(save_note)
add_tag_btn.clicked.connect(add_tag)
delete_tag_btn.clicked.connect(delete_tag)
search_tag_btn.clicked.connect(search_tag)

window.show()
app.exec_()