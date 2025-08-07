"""
The main entry point for client-side code
"""

from pyodide.code import run_js


def window_init():
    """
    Called from the browser to initialize the window.
    """

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
