from orly import app
import os

port = int(os.environ.get('PORT', 5000))

if os.environ.get('IS_PRODUCTION', False):
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)
else:
    app.run(host='0.0.0.0', port=port)
