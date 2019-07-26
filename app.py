from flask import Flask, request, render_template, session, redirect, \
    url_for, jsonify
from flask_mail import Mail
from celery import Celery
from game_logic import Board
import random
import time


app = Flask(__name__)

# Celery configuration
app.config.update({
    'broker_url': 'pyamqp://',
    'result_backend': 'rpc://',
    'timezone': 'Europe/Moscow',
    'imports': (
        'logic.tasks',
    ),
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']
})

# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)


@celery.task
def create_async_board():
    """Create two boards for self and for opponent."""
    context = {}
    board = Board()
    board.fill_board_with_ships()
    opponents_board = Board()
    opponents_board.fill_board_with_ships()
    context['board'] = board.board
    context['opponents_board'] = opponents_board.board
    return context


@celery.task
def asd(x, y):
    print(x+y)
    return x * y


@celery.task
def mark_as_bombed(context, cell):
    context['board'][cell]['is_bombed'] = True


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/warships', methods=['GET', 'POST'])
def warships():
    if request.method == 'GET':
        context = {}
        # context['board1'] = [{'id': _, 'status': 'alive'} for _ in range(1, n)]
        # context['board1'][23]['status'] = 'bombed'
        # context['board1'][35]['status'] = 'ship'
        from game_logic import Board
        board = Board()
        board.fill_board_with_ships()
        opponents_board = Board()
        opponents_board.fill_board_with_ships()
        context['board'] = board.board
        context['opponents_board'] = opponents_board.board
        return render_template('warships.html', context=context)
    if request.form['submit'] == 'Start game':
        # create_async_board.delay()
        return render_template('warships.html')
    else:
        pass
    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()

    return jsonify({}), 202, {
        'Location': url_for('taskstatus', task_id=task.id),
    }


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    context = {}
    board = Board()
    board.fill_board_with_ships()
    opponents_board = Board()
    opponents_board.fill_board_with_ships()
    context['board'] = board.board
    context['opponents_board'] = opponents_board.board
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...',
            'context': context,
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
            'context': context
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
            'context': context
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

