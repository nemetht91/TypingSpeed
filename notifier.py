from typing import Callable


class UpdateNotifier:
    def __init__(self,
                 word_submitted: Callable[[str], None],
                 field_cleared: Callable[[None], None],
                 text_update: Callable[[str], None]):
        self.word_submitted = word_submitted
        self.field_cleared = field_cleared
        self.text_updated = text_update
