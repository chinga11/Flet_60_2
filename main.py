import flet as ft 
from db import main_db


def main(page: ft.Page):
    page.title = 'todo list'
    page.theme_mode = ft.ThemeMode.LIGHT
    task_list = ft.Column(spacing=15) 

    def load_task():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_task():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))
        page.update()

    def create_task_row(task_id, task_text):

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            
        
        
        
        def delete_task(_):
            main_db.delete_task(task_id)
            task_list.controls.remove(row)
            page.update()

        
        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)
        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)
        delet_icon = ft.IconButton(icon=ft.Icons.DELETE,icon_color='red',on_click=delete_task)
        task_field = ft.TextField(value=task_text, read_only=True, expand=True, on_submit=save_task)
   
        row = ft.Row([task_field, edit_button, save_button, delet_icon])
        return row
    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            print(f'Запись сохранена! ID задачи - {task_id}')
            task_input.value = None
            page.update()
    
    


    task_input = ft.TextField(label='Введите задачу', expand=True, on_submit=add_task)
    task_input_button = ft.IconButton(icon=ft.Icons.SEND, on_click=add_task)
    
    main_objects = ft.Row([task_input, task_input_button])

    page.add(main_objects, task_list)
    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)