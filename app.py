from flask import Flask, request, render_template, session, redirect, \
    url_for, jsonify
from flask_mail import Mail
from celery import Celery
from game_logic import Board


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-to-change'


# Celery configuration
app.config['broker_url'] = 'pyamqp://'
app.config['result_backend'] = 'rpc://'
app.config['backend'] = 'rpc://'


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)


@celery.task
def create_async_board():
    """Create two boards for self and for opponent."""
    board1 = Board()
    board2 = Board()
    context = dict()
    board1.fill_board_with_ships()
    board2.fill_board_with_ships()
    context['board1'] = board1
    context['board2'] = board2
    with app.app_context():
        session['context'] = context


@celery.task
def mark_as_bombed(context, cell):
    context['board'][cell]['is_bombed'] = True


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
        create_async_board.delay()
    else:
        pass
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
