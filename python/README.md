# ImAdj = image adjust

A command-line interface (CLI) for rotating and fliping `.bmp` image files

## To run
- `poetry shell` to activate virtual environment
- `poetry run imadj --help` for guidance on CLI options

## For development
- `ptw --run 'pytest'` to automatically run tests when any python files change

## API

ImAdj has a minimal api.
Serve it with hot reloading using `uvicorn imadj.server:app --reload`.

Visit `localhost:8000` in your browser.
