import sublime, sublime_plugin

class VulnCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		window = view.window()		
		file_name = self.view.file_name()
		
		base_path = False
		for project in sublime.active_window().folders():
			if (file_name.startswith(project)):				
				print("Using project %s"%project)
				base_path = project
		if base_path:
			vuln_file_name = "%s\\notes.vuln"%base_path
			new_view = self.view.window().open_file(vuln_file_name)
			# Ugly hack
			if (not new_view.is_dirty()):
				sublime.message_dialog("New notes.vuln (%s)"%vuln_file_name)
				new_view = self.view.window().open_file(vuln_file_name)
		else:
			new_view = sublime.active_window().new_file()
			new_view.set_name("no-project-notes.vuln")
			new_view.set_syntax_file("Packages/User/vuln.tmLanguage")
		

		hdr = "----[ VULN ]-------------------------------------------------------------------\n"
		s = hdr

		for region in view.sel():
			# Get line number.
			pos = region.begin()
			(row, col) = view.rowcol(pos)
			line_num = row + 1

			# Get selection if not empty and full line otherwise.
			if region.empty():
				# Get full line.
				line = view.substr(view.line(pos))
				content = "line: "+line
			else:
				# Get selection.
				selection = view.substr(region)
				content = "selection: "+selection

			position = "\t"+file_name+":"+str(line_num)+"\n"

			s += "\n"+position+content+"\n\n"
			new_view_size = new_view.size()
			# Display results.
			new_view.insert(edit, new_view_size, s)
			# Set selection on hdr text
			new_view.sel().clear()
			new_view.sel().add(sublime.Region(new_view_size+6, new_view_size+10))