"""The main entry point for client-side code."""

from importlib import import_module
from pathlib import Path

from pyodide.code import run_js


def window_init() -> None:
    """Initialize the window. Should be called immediately from the browser."""
    root_style = """
        #root {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #282c34;
            color: white;
        }
    """
    run_js(f"""
        const style = document.createElement('style');
        style.innerHTML = `{root_style}`;
        document.head.appendChild(style);

        const div = document.createElement('div');
        div.innerHTML = '<div id="app">TODO (Created from Python)</div>';
        div.id = 'root';
        document.body.appendChild(div);
    """)


def init_modules() -> None:
    """Import all modules in /src except main.py and call their main()."""
    src_path = Path(__file__).parent
    for file in src_path.iterdir():
        if file.name == "main.py" or file.suffix != ".py":
            continue
        module_name = file.stem
        module = import_module(module_name)
        if hasattr(module, "main"):
            module.main()
