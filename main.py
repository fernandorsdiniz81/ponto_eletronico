import PySimpleGUI as sg
import time
import database_access


class Interface:
	def __init__(self) -> None:
		self.database = database_access.DataBase()
		self.projects = []

	def make_window(self):
		themes = "SystemDefault SystemDefaultForReal SystemDefault1 LightBrown12 DarkGrey10 LightGreen4 Reddit DarkTeal11 DarkGrey7 DarkBlue LightBrown12".split()
		sg.theme("DarkBlue")
		self.projects = [project[0] for project in self.database.read("SELECT projeto FROM principal")]
		self.projects.append("--criar projeto--")
		self.projects.append("--excluir projeto--")
		layout = [
			[sg.Text("Selecione o projeto:", key="select_text"), sg.Combo(values=self.projects, key="combo", enable_events=True)],
			[sg.Text("", key="response"), sg.Input("", key="project_name", visible=False)],
			[sg.Button("iniciar", key="clock", visible=False), sg.Button("criar", key="create", visible=False), sg.Text("registrando...", key="status", visible=False)]
		]

		window = sg.Window("Ponto Eletrônico", layout, size=(300,130))
	
		return window
	

	def open_window(self):
		def hide_elements():
			window["select_text"].update(visible=False)
			window["combo"].update(visible=False)

		def show_elements():
			window["select_text"].update(visible=True)
			window["combo"].update(visible=True)
				
		def update_registry(registry):
			self.database.update(registry)

		window = self.make_window()
		clock_state = False
		
		while True:
			event, value = window.read()

			if event == sg.WIN_CLOSED:
				self.database.close_connection()
				break
			
			elif event == "combo":
				project = value["combo"]
				if project != None and project != "--criar projeto--" and project != "--excluir projeto--":
					window["project_name"].update(visible=False)
					window["create"].update(visible=False)
					window["clock"].update(visible=True)
					window["response"].update(f"Projeto: {project}")
				elif project == "--criar projeto--":
					window["clock"].update(visible=False)
					window["response"].update("Nome do projeto:")
					window["project_name"].update(visible=True)
					window["create"].update(visible=True)
				elif project == "--excluir projeto--":
					exclusion_layout = [[sg.Text("Selecione os projetos a serem excluídos:")]]
					exclusion_layout += [[sg.Checkbox(project, key=f"{project}")] for project in self.projects[:-2]]
					exclusion_layout += [[sg.Button("excluir", key="delete")]]
					exclusion_window = sg.Window("Excluir projetos", exclusion_layout, size=(280,280), resizable=True, relative_location=(310,0))
					while True:
						event, value = exclusion_window.read()
						if event == sg.WIN_CLOSED:
							break
						elif event == "delete":
							projects_to_delete = ""
							for project_name, checked_box in value.items():
								if checked_box == True:
									projects_to_delete += f"'{project_name}',"
							if projects_to_delete != "":
								query = f"DELETE FROM principal WHERE projeto in ({projects_to_delete[:-1]});"
								self.database.delete(query)
								exclusion_window.close()
								window.close()
								self.open_window()
							else:
								exclusion_window.close()


			elif event == "create":
				project_name = value["project_name"]
				query = f"INSERT INTO principal VALUES (0,'{project_name}',0)"
				self.database.create(query)
				window["response"].update("")
				window["project_name"].update(visible=False)
				window["create"].update(visible=False)
				window.close()
				self.open_window()
			
			elif event == "clock":
				if clock_state == False:
					window["clock"].update("finalizar")
					window["status"].update(visible=True)
					clock_state = True
					initial_count = time.time()
					hide_elements()
				else:
					window["clock"].update("iniciar")
					window["status"].update(visible=False)
					clock_state = False
					final_count = time.time()
					total_count = self.database.read(f"SELECT tempo FROM principal WHERE projeto LIKE '{project}'")
					total_count = total_count[0][0]
					total_count += round(final_count - initial_count)
					show_elements()
					query = f"UPDATE principal SET tempo = '{total_count}' WHERE projeto = '{project}'"
					update_registry(query)

		window.close()
	


if __name__ == "__main__":
	ponto_eletronico = Interface()
	ponto_eletronico.open_window()