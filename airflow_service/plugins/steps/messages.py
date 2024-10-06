from airflow.providers.telegram.hooks.telegram import TelegramHook
from airflow.models import Variable


def send_telegram_failure_message(context):
    """Sends a message in case of DAG execution failure."""

    # Instantiating a Telegram hook
    telegram_hook = TelegramHook(
        telegram_conn_id='test',
        token=Variable.get('TELEGRAM_TOKEN_ID'), 
        chat_id=Variable.get('TELEGRAM_CHAT_ID')
    )

    # Defining what information to send
    dag_info = context['dag']
    run_id = context['run_id']
    message = f'DAG {dag_info} with run_id={run_id} failed.'
    
    # Sending a message to Telegram chat
    telegram_hook.send_message({
        'chat_id': Variable.get('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': None,
    })


def send_telegram_success_message(context):
    """Sends a message in case of DAG execution success."""
    
    telegram_hook = TelegramHook(
        telegram_conn_id='test', 
        token=Variable.get('TELEGRAM_TOKEN_ID'),
        chat_id=Variable.get('TELEGRAM_CHAT_ID')
    )

    dag_info = context['dag']
    run_id = context['run_id']
    message = f'DAG {dag_info} with run_id={run_id} finished successfully.'
    
    telegram_hook.send_message({
        'chat_id': Variable.get('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': None,
    })