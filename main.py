from flet import * 
from database import DatabaseManager
import markdown2
DM = DatabaseManager("database.db")

class Note(UserControl):
    """docstring for Note"""
    def __init__(self):
        super().__init__()
        newnotetext = DM.create_new_note()
        self.i = newnotetext[0]
        self.pagedrawerindex = 0
        self.myinput = TextField(
            multiline=True,
            min_lines=1,
            filled = False,
            hint_text="Title",
            hint_style = TextStyle(size = 32),
            text_size = 18,
            selection_color= "gray",
            color="#E8E9E4",
            border= InputBorder.NONE,
            on_change = self.saving,            

        )

    def NewNote(self, e = 0):
        newnotetext = DM.create_new_note()
        self.i = newnotetext[0]
        self.myinput.value = newnotetext[4]
        self.myinput.update()


    def saving(self, e):
        text = self.myinput.value
        if len(text) != 0:   
            DM.save_to_database(text, self.i)
        


    def build(self):
        return Container(
                margin = 0,
                content = self.myinput
                )
        



def main(page:Page):
    page.window_width = 700
    page.window_height = 500
    note = Note()
    page.bgcolor = "#060503"
    page.scroll = "AUTO"
    page.title = "Panotion"


    def switch_betwen_notes(e):
        emptynote = None
        if note.myinput.value == "":
            emptynote = note.i
        note.pagedrawerindex = e.control.selected_index
        text = DM.click_note(e.control.selected_index)
        note.i = text[0]
        note.myinput.value = text[4]
        note.myinput.color = text[5]
        note.myinput.update()
        close_drawer()
        if emptynote:
            DM.delete_note(emptynote)


    def showme_drawer(e):
        page.drawer.open = True
        page.drawer.controls = showNotes()
        page.drawer.update()

    def close_drawer():
        page.drawer.open = False
        page.drawer.update()


    def get_all_notes():
        allNotes = DM.get_all_notes()
        return allNotes


    def showNotes():
        controls = [
            Container(height=15),
                TextButton("New note", icon="note_add", on_click = lambda e: (note.NewNote(e), close_drawer())
                ),
            Divider(thickness=2),
        ]
        destination_list = []
        for i in get_all_notes():
            destination = NavigationDrawerDestination(
                label=f"{i[3]}",  
                icon="note",
                selected_icon_content=Icon(icons.NOTE, color = "#DCB13b"),
            )
            destination_list.append(destination)
        
        
        controls.extend(destination_list)
        return controls


    def text_size_plus(e):
        note.myinput.text_size += 1
        note.myinput.update()

    def text_size_minus(e):
        note.myinput.text_size -= 1
        note.myinput.update()


    def text_color(color):
        note.myinput.color = color
        note.myinput.update()
        DM.save_text_color(color, note.i)

    def delete_note(e):
        DM.delete_note(note.i)
        if len(page.drawer.controls) > 4:
            text = DM.click_note(note.pagedrawerindex)
            note.i = text[0]
            note.myinput.value = text[4]
            note.myinput.color = text[5]
            note.myinput.update()
        else:
            note.NewNote()


    def mysavefile(e: FilePickerResultEvent):
        save_location = e.path
        if save_location:
            try:
                with open(save_location, "w", encoding="utf8") as file:
                    print("save succes")
                    file.write(note.myinput.value)
            except Exception as e:
                print("error saved", e)
        page.update()

    saveme = FilePicker(on_result=mysavefile)
    page.overlay.append(saveme)


    page.drawer = NavigationDrawer(
        bgcolor = "#1C1C1E",
        elevation = 40,
        indicator_color = "#1C1C1E",
        indicator_shape = StadiumBorder(),
        shadow_color = "gray500",
        selected_index=0,
        on_change=switch_betwen_notes,
        controls = showNotes()

        )


    colors = [
        ("#E8E9E4", "Default"),
        ("#787774", "Gray"),
        ("#9F6B53", "Brown"),
        ("#D9730D", "Orange"),
        ("#CB912F", "Yellow"),
        ("#448361", "Green"),
        ("#337EA9", "Blue"),
        ("#9065B0", "Purple"),
        ("#C14C8A", "Pink"),
        ("#D44C47", "Red"),
    ]


    page.add(note,

        AppBar(
            title=Text("PANOTION", color = "white", size = 30, weight=FontWeight.W_600),
            bgcolor = "#2D2B2C",
            actions=[
                IconButton(icons.TEXT_INCREASE_ROUNDED, on_click = text_size_plus),

                IconButton(icons.TEXT_DECREASE_ROUNDED, on_click = text_size_minus),

                IconButton(icon = icons.SAVE_AS_SHARP,tooltip = "Save as...", on_click=lambda _: saveme.save_file(file_name="myfile.txt")),

                IconButton(icon = icons.DELETE, tooltip = "Delete note", on_click = delete_note),

                PopupMenuButton(icon = icons.FORMAT_COLOR_TEXT_ROUNDED,
                    items = [
                        PopupMenuItem(content=Row([Icon(icons.FORMAT_COLOR_TEXT_ROUNDED, color=color), Text(name)]),  on_click=lambda _, color=color: text_color(color))
                        for color, name in colors
                    ],
                )
            ],

            leading = IconButton(icon="menu",
                on_click = showme_drawer
            ),

        ),
    )


app(target=main)