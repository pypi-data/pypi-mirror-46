# -*- coding: utf-8 -*-
class TingTingImplementationException(Exception):
    def __init__(self, msg):

        super(TingTingImplementationException, self).__init__(msg)


class TingInitException(Exception):
    def __init__(self, msg):
        super(TingException, self).__init__(msg)


class TingException(Exception):
    def __init__(self, ting, attribute_name, parent_exception):

        self.ting = ting
        self.attribute_name = attribute_name

        self.exc_chain = None
        self.attribute_chain = None

        root_exc = parent_exception
        self.exc_chain = [self]
        self.attribute_chain = [self.attribute_name]

        while (
            isinstance(root_exc, TingException)
            and root_exc.parent_exception is not None
        ):
            self.exc_chain.append(root_exc)
            self.attribute_chain.append(root_exc.attribute_name)
            root_exc = root_exc.parent_exception

        self.root_exc = root_exc

        self.msg = "Can't compute attribute '{}' for item '{}': {}".format(
            attribute_name, ting.id, self.root_exc
        )

        self.parent_exception = parent_exception
        super(TingException, self).__init__(self.msg)
