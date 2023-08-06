from .nb_helper import ASPRules
from .run_clingo import run_clingo

import notebook
import shutil
import IPython
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, line_cell_magic, Magics, magics_class
import os


@magics_class
class PWENBMagics(Magics):

    @staticmethod
    def load(v, user_ns):
        lines = []
        if os.path.exists(v):
            with open(v, 'r') as f:
                lines = f.read().splitlines()
        elif v in user_ns:
            temp = user_ns[v]
            if isinstance(temp, list):
                lines = temp
            elif isinstance(temp, str):
                lines = temp.splitlines()
        return lines

    @staticmethod
    def save(lines, loc, user_ns):

        def is_a_valid_textfile_name(loc: str):
            return loc.find('.') != -1

        if is_a_valid_textfile_name(loc):
            with open(loc, 'w') as f:
                if isinstance(lines, list):
                    f.write("\n".join(lines))
                elif isinstance(lines, str):
                    f.write(lines)
        else:
            user_ns[loc] = lines

    @staticmethod
    def clean_fname(fname: str):
        return fname.strip('\"').strip("\'")

    @line_cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('-l', '--loadfrom', nargs='+', type=str, default=[])
    @magic_arguments.argument('-s', '--saveto', type=str, default=None)
    @magic_arguments.argument('--save_meta_data_to', type=str, default=None)
    @magic_arguments.argument('-n', '--num_solutions', type=int, default=0)
    @magic_arguments.argument('-lci', '--load_combined_input_to', type=str, default=None)
    @magic_arguments.defaults(display_input=True)
    @magic_arguments.argument('--display_input', dest='display_input', action='store_true')
    @magic_arguments.argument('--donot-display_input', dest='display_input', action='store_false')
    @magic_arguments.defaults(display_output=True)
    @magic_arguments.argument('--display_output', dest='display_output', action='store_true')
    @magic_arguments.argument('--donot-display_output', dest='display_output', action='store_false')
    @magic_arguments.defaults(run=True)
    @magic_arguments.argument('--run', dest='run', action='store_true')
    @magic_arguments.argument('--donot-run', dest='run', action='store_false')
    @magic_arguments.argument('-exp', '--experiment_name', type=str, default=None)
    def clingo(self, line='', cell=None):

        output = {}

        args = magic_arguments.parse_argstring(self.clingo, line)
        clingo_program = []
        if args.loadfrom:
            for v in args.loadfrom:
                clingo_program += PWENBMagics.load(v, self.shell.user_global_ns)
        if cell:
            clingo_program += cell.splitlines()

        if args.load_combined_input_to:
            PWENBMagics.save(clingo_program, args.load_combined_input_to, self.shell.user_global_ns)

        if args.display_input:
            print("Clingo Program")
            display(ASPRules("\n".join(clingo_program)))

        output['asp_rules'] = clingo_program

        if args.run:
            clingo_soln, md = run_clingo(clingo_program, args.num_solutions)
            if args.display_output:
                print("Clingo Solution")
                display(ASPRules("\n".join(clingo_soln)))

            if args.saveto:
                PWENBMagics.save(clingo_soln, args.saveto, self.shell.user_global_ns)

            if args.save_meta_data_to:
                PWENBMagics.save(md, args.save_meta_data_to, self.shell.user_global_ns)

            output['asp_soln'] = clingo_soln
            output['meta_data'] = md

        if args.experiment_name:
            self.shell.user_global_ns[args.experiment_name] = output


    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('fnames', nargs='+', type=str, default=[])
    @magic_arguments.argument('-r', '--reasoner', type=str, choices=['clingo', 'dlv'], default='clingo')
    @magic_arguments.defaults(edit=False)
    @magic_arguments.argument('-e', '--edit', dest='edit', action='store_true', help='Only works when one file is provided')
    @magic_arguments.argument('-no-e', '--no-edit', dest='edit', action='store_false')
    def asp_loadfiles(self, line=''):
        args = magic_arguments.parse_argstring(self.asp_loadfiles, line)
        if not args.fnames:
            print("No filenames provided")
            return
        code_lines = []
        for fname in args.fnames:
            fname = PWENBMagics.clean_fname(fname)
            with open(fname, 'r') as f:
                code_lines.extend(f.read().splitlines())
        options = []
        options.append('--run')
        if args.edit and len(args.fnames) == 1:
            options.append('--load_combined_input_to {}'.format(args.fnames[0]))
        contents = '%%clingo {}\n%asp_loadfiles {}\n\n{}'.format(" ".join(options), " ".join(args.fnames), "\n".join(code_lines))
        self.shell.set_next_input(contents, replace=True)


def load_prolog_js_files():
    codemirror_modes_location = os.path.join(notebook.DEFAULT_STATIC_FILES_PATH, 'components', 'codemirror', 'mode')
    codemirror_prolog_location = '{}/prolog/'.format(codemirror_modes_location)
    os.makedirs(codemirror_prolog_location, exist_ok=True)
    for fname in os.listdir('prolog'):
        shutil.copy2('prolog/{}'.format(fname), codemirror_prolog_location)


def load_ipython_extension(ipython):
    #load_prolog_js_files()
    js = "IPython.CodeCell.options_default.highlight_modes['prolog'] = {'reg':[/^%%clingo/]};"
    IPython.core.display.display_javascript(js, raw=True)
    ipython.register_magics(PWENBMagics)