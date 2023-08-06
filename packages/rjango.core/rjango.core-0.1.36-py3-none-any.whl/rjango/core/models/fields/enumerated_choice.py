from .. import models


class EnumeratedChoiceField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 24
        kwargs["db_index"] = True
        kwargs["null"] = False
        kwargs["blank"] = False

        super().__init__(*args, **kwargs)

    def validate(self, *args, **kwargs):
        super().validate(*args, **kwargs)
