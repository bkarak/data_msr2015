

class ProjectStatus(object):
    def __init__(self, project_name):
        self.__project_name = project_name
        self.__clmt_import = False
        self.__jdepend_import = False
        self.__ckjm_import = False

    def get_project_name(self):
        return self.__project_name

    def __set_clmt(self, value):
        if self.__clmt_import:
            raise Exception('CLMT project already set (%s)' % (self.__project_name,))

        self.__clmt_import = True

    def __get_clmt(self):
        return self.__clmt_import

    def __set_jdepend(self, value):
        if self.__jdepend_import:
            raise Exception('JDepend project already set (%s)' % (self.__project_name,))

        self.__jdepend_import = True

    def __get_jdepend(self):
        return self.__jdepend_import

    def __set_ckjm(self, value):
        if self.__ckjm_import:
            raise Exception('CKJM project already set (%s)' % (self.__project_name,))

        self.__ckjm_import = True

    def __get_ckjm(self):
        return self.__ckjm_import

    clmt_imported = property(__get_clmt, __set_clmt)
    jdepend_imported = property(__get_jdepend, __set_jdepend)
    ckjm_imported = property(__get_ckjm, __set_ckjm)
