from peewee import SqliteDatabase, Model, CharField, TextField, BigIntegerField
import atexit
from pynput import keyboard
import pyautogui
import re

location = './data.db'
table_name = 'snippets'


if __name__ == '__main__':

    prev_key = None
    prev_prev_key = None
    result = None
    typed_chars = []
    is_record = True

    db = SqliteDatabase('./data.db')

    def exit_handler():
        db.close()
        print('Exiting Program Gracefully!')
        quit(0)

    atexit.register(exit_handler)

    class Snippet(Model):
        key = CharField()
        value = TextField()
        freq = BigIntegerField()

        class Meta:
            database = db

    if not Snippet.table_exists():
        Snippet.create_table()

    def check():
        global typed_chars
        global result
        word = ''.join(typed_chars)
        pattern = re.compile('[\W_]+')
        pattern.sub('', word)
        result = Snippet.select().where(Snippet.key == word)
        if result.exists():
            return True

    def assist():
        global result
        global typed_chars
        global is_record
        t = result.get().value
        is_record = False
        for _ in typed_chars:
            pyautogui.press('backspace')
        pyautogui.typewrite(t, interval=0.0)
        pyautogui.press('space')
        typed_chars = []
        is_record = True

    def on_press(key):

        global is_record
        global prev_key
        global prev_prev_key
        global typed_chars

        if not is_record:
            return True

        try:

            if key.char == 'c' and prev_key == keyboard.Key.shift_l and prev_prev_key == keyboard.Key.ctrl_l:
                return False

            pattern = re.compile('\w')
            is_ok = pattern.match(key.char)

            if is_ok:
                typed_chars.append(key.char)

            if key.char == '=':
                if check():
                    pyautogui.press('backspace', interval=0.0)
                    assist()

        except AttributeError:

            if key == keyboard.Key.space:
                typed_chars = []

            if key == keyboard.Key.backspace \
                    and (not prev_prev_key == keyboard.Key.ctrl_l) \
                    and len(typed_chars) > 0:
                typed_chars.pop()

            if key == keyboard.Key.f8:
                if check():
                    assist()

            if key == keyboard.Key.backspace and prev_prev_key == keyboard.Key.ctrl_l:
                if hasattr(prev_key, 'char'):
                    if prev_key.char == '\x01':
                        typed_chars = []

        finally:
            prev_prev_key = prev_key
            prev_key = key


    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
