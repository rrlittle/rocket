from typing import *
import sys
from tkinter import filedialog

class BasedContext:
    def get_filepath(self,
                     save=False,  # This flag is used to specify whether the file is for output or input
                     title='open file',
                     filetype='file',
                     quit=True,
                     allownew=True,
                     **kwargs) -> Optional[str]:
        """this is a generic function that can be extended
            it simply gets a filepath and asserts it's not empty.
            if it's empty the program quits unless quit is False.
            when it will throw an error

            filetype is a string used for error messages and variable names

            askopenfilename takes other kwargs as well you can look into
            all of them provided get passed on.
            - defaultextension - str expression for default extensions
            - others check out utils.askopenfilename docs for more
            - initialdir - str path to where you would like to open
            - initialfile - str default filename

            TODO: figure out how to disallow new files being made/ allow
        """
        fpath = None
        # I have hard coded the file types to csv and tsv.
        if save:
            fpath = filedialog.asksaveasfilename(title=title, filetypes=(("csv files", "*.csv"),
                                                                         ("all files", "*.*")),
                                                 **kwargs)
        else:
            fpath = filedialog.askopenfilename(title=title, filetypes=(("all files", "*.*"),
                                                                       ("tsv files", "*.tsv"),
                                                                       ("csv files", "*.csv"),),
                                               **kwargs)

        # Check path validity
        if fpath == '' or len(fpath) == 0:
            print('no %s file selected. quitting' % filetype)
            return None

        setattr(self, filetype, fpath)
        return fpath


class TemplateOnlyContext(BasedContext):
    """
        This class is used to hold the file paths for necessary components in the running of rocket.
        Currently, it holds the template path. Subclass will be used for COINs and streamline versions of rocket
    """

    def __init__(self, template_path=None):
        super().__init__()

        # None always means uninitialized
        self.template_path = template_path  # type: Optional[str]

    def get_template_path(self, based_dir_for_userinput="") -> Optional[str]:
        return self.template_path


class UserInputTemplateOnlyContext(TemplateOnlyContext):

    def __init__(self, template_path):
        super(UserInputTemplateOnlyContext, self).__init__(template_path)

    def get_template_path(self, based_dir_for_userinput="") -> Optional[str]:
        if self.template_path is None:
            self.template_path = self.get_filepath(title="Template",
                                                   initialdir=based_dir_for_userinput,
                                                   save=False,
                                                   filetype='templates',
                                                   allownew=True)
        return self.template_path


class SourceDataPathOnlyContext(BasedContext):
    def __init__(self, data_path=None):
        super(SourceDataPathOnlyContext, self).__init__()
        self.data_path = data_path  # type: Optional[str]

    def get_source_data_path(self, default_data_dir="") -> Optional[str]:
        return self.data_path
    
    
class UserInputSourceDataOnlyContext(SourceDataPathOnlyContext):
    def __init__(self, data_path=None):
        super(UserInputSourceDataOnlyContext, self).__init__(data_path)
    
    def get_source_data_path(self, default_data_dir=""):
        if self.data_path is None:
            self.data_path = self.get_filepath(filetype='srcpath',
                                                   initialdir=default_data_dir,
                                                   title='select the source data file')

        return self.data_path


class TemplateAndSourceDataContext(TemplateOnlyContext, SourceDataPathOnlyContext):
    def __init__(self, template_path, data_path):
        TemplateOnlyContext.__init__(self, template_path)
        SourceDataPathOnlyContext.__init__(self, data_path)


class UserInputTemplateAndSourceDataContext(UserInputTemplateOnlyContext, UserInputSourceDataOnlyContext):
    def __init__(self, template_path = None, data_path = None):
        UserInputTemplateOnlyContext.__init__(self, template_path)
        UserInputSourceDataOnlyContext.__init__(self, data_path)


if __name__ == "__main__":
    t = UserInputTemplateAndSourceDataContext()
    print(t.get_template_path(), t.get_source_data_path())