from werkzeug.local import LocalStack, LocalProxy


class ContextNotAvailable(Exception):
    pass


class ContextStack:

    _local_stack = LocalStack()

    @staticmethod
    def get_context():
        _context = ContextStack._local_stack.top

        if not _context:
            raise ContextNotAvailable("You are not in a Context.")

        return _context

    def __init__(self, **kwargs):
        super().__init__()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __add__(self, other):
        return self.clone(**other.__dict__)

    def __enter__(self):
        ContextStack._local_stack.push(self)
        return self

    def __exit__(self, *args):
        ContextStack._local_stack.pop()

    def get(self, name: str, default=None):
        if hasattr(self, name):
            return getattr(self, name)

        return default

    def clone(self, **new_values):
        return ContextStack(**{**self.__dict__, **new_values})

    def push(self):
        return self.__enter__()

    def pop(self):
        self.__exit__()


ctx = LocalProxy(ContextStack.get_context)


class ContextCloneHelper:

    def __call__(self, clone=True, **kwargs):
        try:
            in_ctx = bool(ctx)
        except ContextNotAvailable:
            in_ctx = False

        if in_ctx and clone:
            return ctx.clone(**kwargs)

        return ContextStack(**kwargs)


Context = ContextCloneHelper()
