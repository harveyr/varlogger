# http://www.sublimetext.com/docs/commands
# http://www.sublimetext.com/docs/2/api_reference.html

import sublime
import sublime_plugin
import re


class LogvarCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print(self.current_scope())
        var_name = self.get_cursor_word()
        if var_name is not None:
            self.insert_with_newline(edit, self.log_str(var_name))

    def log_str(self, var_name):
        ws = self.leading_whitespace()
        trimmed = self.trim_quoted_output(var_name)

        if self.in_python():
            log_cmd = self.get_python_log_command()
            return ("{ws}{cmd}('{trimmed}: {{v}}'.format(v={var}))").format(
                ws=ws, cmd=log_cmd, trimmed=trimmed, var=var_name)

        if self.in_js():
            return ("{0}console.log('{1}:', {2});").format(
                ws, trimmed, var_name)

        if self.in_coffee():
            return ("{0}console.log '{1}:', {2}").format(ws, trimmed, var_name)

        if self.in_go():
            return('{0}log.Print("{1}: ", {2})'.format(ws, trimmed, var_name))

        if self.in_php():
            return (
                '{0}print("\\n-----\\n" . \'{1}:\'); ' +
                'var_dump({2}); ' +
                'print("\\n-----\\n"); ' +
                "ob_flush();").format(ws, trimmed, var_name)

    def trim_quoted_output(self, output):
        return re.sub(r'\'|\"', '', output)

    def insert_with_newline(self, edit, text):
        view = self.active_view()
        eol = view.line(view.sel()[0]).end()
        self.view.insert(edit, eol, "\n{}".format(text))

    def get_python_log_command(self):
        view = self.active_view()
        match = view.find(r'(\w+) = logging\.getLogger', 0)
        print('match: {v}'.format(v=match))
        if match.a >= 0:
            word = view.substr(view.word(match.a))
            return '{logger}.debug'.format(logger=word)
        return 'print'

    def get_cursor_word(self):
        view = self.active_view()
        word = view.substr(view.sel()[0]).strip()
        if len(word) == 0:
            return None
        return word

    def leading_whitespace(self):
        view = self.active_view()
        line = view.substr(view.line(view.sel()[0]))
        matches = re.findall(r'(\s*)\S+', line)
        return matches[0]

    def in_python(self):
        return 'python' in self.current_scope()

    def in_php(self):
        return 'source.php' in self.current_scope()

    def in_js(self):
        return 'source.js' in self.current_scope()

    def in_coffee(self):
        return 'source.coffee' in self.current_scope()

    def in_go(self):
        return 'source.go' in self.current_scope()

    def current_scope(self):
        print(self.active_view().scope_name(0))
        return self.active_view().scope_name(0)

    def active_view(self):
        return sublime.active_window().active_view()

    def get_view_contents(self):
        view = self.active_view()
        return view.substr(sublime.Region(0, view.size()))
