from .exceptions import ValidationError


class Command(type):
    def parser(cls):
        """
        Return:
            A parser used to check command format, and return parsed arguments.
        """
        raise NotImplementedError("You must implement a parser for this command")

    def validate(cls, args):
        """
        Implement extra validation for parsed arguments if required...
        """

    def run(cls, **args):
        raise NotImplementedError("You must implement 'run' method for this command")
    
    def __call__(cls):
        parser = cls.parser()
        args = parser.parse_args()

        try:
            cls.validate(args)
        except ValidationError as e:
            parser.print_help()
            print('[Error]', str(e))
            exit(0)
        
        cls.run(**vars(args))
