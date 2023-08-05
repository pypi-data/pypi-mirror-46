import logging as _logging
from ..utils import Command, Call
from ..error import NoneFoundError, \
                    TooManyFoundError, \
                    UnregisteredError, \
                    UnsupportedError, \
                    InvalidInputError, \
                    InvalidConfigError, \
                    RoyalnetError, \
                    ExternalError


log = _logging.getLogger(__name__)


class ErrorHandlerCommand(Command):

    command_name = "error_handler"
    command_description = "Gestisce gli errori causati dagli altri comandi."
    command_syntax = ""

    @classmethod
    async def common(cls, call: Call):
        exception: Exception = call.kwargs["exception"]
        if isinstance(exception, NoneFoundError):
            await call.reply(f"⚠️ L'elemento richiesto non è stato trovato.\n[p]{exception}[/p]")
            return
        if isinstance(exception, TooManyFoundError):
            await call.reply(f"⚠️ La richiesta effettuata è ambigua, pertanto è stata annullata.\n[p]{exception}[/p]")
            return
        if isinstance(exception, UnregisteredError):
            await call.reply("⚠️ Devi essere registrato a Royalnet per usare questo comando.\nUsa il comando [c]sync[/c] per registrarti!")
            return
        if isinstance(exception, UnsupportedError):
            await call.reply(f"⚠️ Il comando richiesto non è disponibile tramite l'interfaccia [c]{call.interface_name}[/c].")
            return
        if isinstance(exception, InvalidInputError):
            command = call.kwargs["previous_command"]
            await call.reply(f"⚠️ Sintassi non valida.\nSintassi corretta: [c]{call.interface_prefix}{command.command_name} {command.command_syntax}[/c]")
            return
        if isinstance(exception, InvalidConfigError):
            await call.reply(f"⚠️ Il bot non è stato configurato correttamente, quindi questo comando non può essere eseguito.\n[p]{exception}[/p]")
            return
        if isinstance(exception, RoyalnetError):
            await call.reply(f"⚠️ La richiesta a Royalnet ha restituito un errore: [p]{exception.exc}[/p]")
            return
        if isinstance(exception, ExternalError):
            await call.reply(f"⚠️ Una risorsa esterna necessaria per l'esecuzione del comando non ha funzionato correttamente, quindi il comando è stato annullato.\n[p]{exception}[/p]")
            return
        await call.reply(f"❌ Eccezione non gestita durante l'esecuzione del comando:\n[b]{exception.__class__.__name__}[/b]\n[p]{exception}[/p]")
        log.error(f"Unhandled exception - {exception.__class__.__name__}: {exception}")
