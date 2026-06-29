import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

class TargetBlankProcessor(Treeprocessor):
    def run(self, root) -> None:
        for a in root.iter('a'):
            a.set('target', '_blank')
            a.set('rel', 'noopener noreferrer')

class TargetBlankExtension(Extension):
    def extendMarkdown(self, md) -> None:
        md.treeprocessors.register(TargetBlankProcessor(md), 'target_blank', 15)

def tasks_to_md(tasks: list[dict]) -> str:
    md_content = ''
    ticket_link = 'https://tickets.inescop.es/scp/tickets.php?a=search&search-type=&query='
    
    pending_tasks = [task for task in tasks if not task['done']]
    done_tasks = [task for task in tasks if task['done']]
    
    for n_task, task in enumerate(pending_tasks):
        md_content += f'## {n_task + 1}. {task["name"]}\n'
        md_content += f'* **Date:** {task["addition_date"]}\n'
        if task['ticket']:
            md_content += f'* **Ticket:** '
            md_content += f'[#{task["ticket"]}]'
            md_content += f'({ticket_link}{task["ticket"]})\n'
        md_content += f'* **Description:** {task["description"]}\n'
        
        for n_note, note in enumerate(task['notes']):
            if n_note == 0:
                md_content += f'* **Notes:**\n'
            md_content += f'\t* {note}'
            md_content += '\n'
            
        md_content += '\n'
    
    md_content += '\n---\n'
    md_content += '## Completed tasks\n'
    for task in done_tasks:
        md_content += f'* *[{task["done"]}] {task["name"]}\n'
        if task['ticket']:
            md_content += f'([#{task["ticket"]}]({ticket_link}{task["ticket"]}))*\n'
        else:
            md_content += '*\n'
    
    return md_content

def render_task_md(md_content: str) -> str:
    rendered_md = markdown.markdown(
        md_content,
        extensions=['extra', 'sane_lists', 'smarty', 'toc', TargetBlankExtension()],
        output_format='html5'
    )
    
    # html = f"""<!DOCTYPE html>
    # <html lang="es">
    # <head>
    #     <meta charset="UTF-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <title>Render document</title>
    #     <style>
    #         :root {{
    #             --bg-color: #ffffff;
    #             --text-color: #374151; /* Gris oscuro elegante */
    #             --heading-color: #111827; /* Casi negro para contraste */
    #             --border-color: #e5e7eb;
    #             --code-bg: #f3f4f6;
    #             --accent-color: #4b5563;
    #         }}

    #         body {{
    #             font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    #             line-height: 1.8;
    #             color: var(--text-color);
    #             background-color: var(--bg-color);
    #             max-width: 850px;
    #             margin: 0 auto;
    #             padding: 50px 30px;
    #             font-size: 16px;
    #         }}

    #         h1, h2, h3, h4, h5, h6 {{
    #             font-family: "Georgia", "Times New Roman", serif;
    #             color: var(--heading-color);
    #             margin-top: 2.5em;
    #             margin-bottom: 0.75em;
    #             font-weight: 400;
    #         }}

    #         h1 {{
    #             font-size: 2.5em;
    #             text-align: center;
    #             border-bottom: 1px solid var(--border-color);
    #             padding-bottom: 20px;
    #             margin-top: 1em;
    #         }}

    #         h2 {{
    #             font-size: 1.8em;
    #             border-bottom: 1px solid var(--border-color);
    #             padding-bottom: 10px;
    #         }}

    #         h3 {{
    #             font-size: 1.4em;
    #         }}

    #         p {{
    #             margin-bottom: 1.5em;
    #         }}

    #         a {{
    #             color: var(--accent-color);
    #             text-decoration: none;
    #             border-bottom: 1px dotted var(--accent-color);
    #             transition: color 0.2s ease;
    #         }}

    #         a:hover {{
    #             color: var(--heading-color);
    #             border-bottom: 1px solid var(--heading-color);
    #         }}

    #         blockquote {{
    #             margin: 2em 0;
    #             padding: 1em 2em;
    #             border-left: 4px solid var(--accent-color);
    #             background-color: #f9fafb;
    #             font-style: italic;
    #             color: #4b5563;
    #         }}

    #         table {{
    #             width: 100%;
    #             border-collapse: collapse;
    #             margin: 2em 0;
    #             font-size: 0.95em;
    #         }}

    #         th, td {{
    #             padding: 12px 15px;
    #             border-bottom: 1px solid var(--border-color);
    #             text-align: left;
    #         }}

    #         th {{
    #             font-family: "Georgia", serif;
    #             font-weight: normal;
    #             color: var(--heading-color);
    #             background-color: #f9fafb;
    #         }}

    #         code {{
    #             font-family: "Consolas", "Monaco", "Courier New", monospace;
    #             background-color: var(--code-bg);
    #             padding: 0.2em 0.4em;
    #             border-radius: 4px;
    #             font-size: 0.9em;
    #             color: #be185d; /* Un tono sutil para el código inline */
    #         }}

    #         pre {{
    #             background-color: var(--code-bg);
    #             padding: 20px;
    #             border-radius: 8px;
    #             overflow-x: auto;
    #             border: 1px solid var(--border-color);
    #             margin: 2em 0;
    #         }}

    #         pre code {{
    #             background-color: transparent;
    #             padding: 0;
    #             color: inherit;
    #             border: none;
    #         }}

    #         ul, ol {{
    #             margin-bottom: 1.5em;
    #             padding-left: 2em;
    #         }}

    #         li {{
    #             margin-bottom: 0.5em;
    #         }}

    #         img {{
    #             max-width: 100%;
    #             height: auto;
    #             border-radius: 8px;
    #             margin: 2em 0;
    #             display: block;
    #         }}
    #     </style>
    # </head>
    # <body>
    #     {markdown.markdown(md_content)}
    # </body>
    # </html>
    # """
    
    html = f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tasks</title>

        <style>
            :root {{
                --page-bg: #f6f3ee;
                --page-bg-soft: #fbfaf7;
                --paper-bg: #fffdf9;

                --text: #2f3437;
                --text-soft: #5f6b73;
                --heading: #111315;
                --muted: #7b858c;

                --accent: #8a6f3d;
                --accent-soft: rgba(138, 111, 61, 0.13);

                --border: #e5ded2;
                --border-strong: #d3c7b6;

                --code-bg: #f3efe8;
                --code-text: #7a2e4d;

                --shadow: 0 24px 70px rgba(25, 22, 18, 0.10);
                --radius: 22px;
            }}

            @media (prefers-color-scheme: dark) {{
                :root {{
                    --page-bg: #11100e;
                    --page-bg-soft: #171512;
                    --paper-bg: #1f1c18;

                    --text: #e8e2d8;
                    --text-soft: #c8bfb2;
                    --heading: #fffaf2;
                    --muted: #a99f91;

                    --accent: #d5b36c;
                    --accent-soft: rgba(213, 179, 108, 0.14);

                    --border: #3b352c;
                    --border-strong: #5a4d3d;

                    --code-bg: #2a251f;
                    --code-text: #f0a6c2;

                    --shadow: 0 24px 70px rgba(0, 0, 0, 0.35);
                }}
            }}

            * {{
                box-sizing: border-box;
            }}

            html {{
                scroll-behavior: smooth;
            }}

            body {{
                margin: 0;
                min-height: 100vh;
                color: var(--text);
                background:
                    radial-gradient(circle at top left, rgba(138, 111, 61, 0.16), transparent 34rem),
                    linear-gradient(180deg, var(--page-bg-soft), var(--page-bg));
                font-family:
                    Inter,
                    Aptos,
                    -apple-system,
                    BlinkMacSystemFont,
                    "Segoe UI",
                    Roboto,
                    Helvetica,
                    Arial,
                    sans-serif;
                font-size: 17px;
                line-height: 1.78;
                letter-spacing: -0.006em;
                padding: 48px 20px;
            }}

            .document {{
                width: min(100%, 920px);
                margin: 0 auto;
                padding: clamp(34px, 6vw, 78px);
                background: var(--paper-bg);
                border: 1px solid var(--border);
                border-radius: var(--radius);
                box-shadow: var(--shadow);
            }}

            .document > *:first-child {{
                margin-top: 0;
            }}

            .document > *:last-child {{
                margin-bottom: 0;
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: var(--heading);
                font-family:
                    "Iowan Old Style",
                    "Palatino Linotype",
                    Palatino,
                    Georgia,
                    serif;
                font-weight: 500;
                line-height: 1.18;
                letter-spacing: -0.035em;
                text-wrap: balance;
            }}

            h1 {{
                max-width: 760px;
                margin: 0 auto 1.4em;
                padding-bottom: 0.65em;
                border-bottom: 1px solid var(--border-strong);
                font-size: clamp(2.35rem, 6vw, 4.1rem);
                text-align: center;
            }}

            h1::after {{
                content: "";
                display: block;
                width: 76px;
                height: 3px;
                margin: 0.55em auto 0;
                border-radius: 99px;
                background: var(--accent);
            }}

            h2 {{
                margin-top: 2.4em;
                margin-bottom: 0.7em;
                padding-bottom: 0.35em;
                border-bottom: 1px solid var(--border);
                font-size: clamp(1.6rem, 3vw, 2.1rem);
            }}

            h3 {{
                margin-top: 2em;
                margin-bottom: 0.55em;
                font-size: 1.35rem;
            }}

            h4 {{
                margin-top: 1.7em;
                margin-bottom: 0.45em;
                font-size: 1.08rem;
                letter-spacing: 0.01em;
                text-transform: uppercase;
            }}

            p {{
                margin: 1.05em 0;
            }}

            strong {{
                color: var(--heading);
                font-weight: 700;
            }}

            em {{
                color: var(--text-soft);
            }}

            a {{
                color: var(--heading);
                text-decoration: none;
                background:
                    linear-gradient(var(--accent-soft), var(--accent-soft))
                    0 88% / 100% 0.42em no-repeat;
                border-bottom: 1px solid rgba(138, 111, 61, 0.35);
                transition:
                    background-size 160ms ease,
                    border-color 160ms ease,
                    color 160ms ease;
            }}

            a:hover {{
                color: var(--accent);
                background-size: 100% 0.72em;
                border-color: var(--accent);
            }}

            a:focus-visible {{
                outline: 3px solid var(--accent-soft);
                outline-offset: 3px;
                border-radius: 4px;
            }}

            hr {{
                width: 42%;
                margin: 3.2em auto;
                border: 0;
                border-top: 1px solid var(--border-strong);
            }}

            blockquote {{
                position: relative;
                margin: 2.1em 0;
                padding: 1.15em 1.35em 1.15em 1.65em;
                color: var(--text-soft);
                background: var(--accent-soft);
                border-left: 4px solid var(--accent);
                border-radius: 0 16px 16px 0;
                font-family:
                    "Iowan Old Style",
                    "Palatino Linotype",
                    Palatino,
                    Georgia,
                    serif;
                font-size: 1.08em;
                line-height: 1.7;
            }}

            blockquote p {{
                margin: 0.65em 0;
            }}

            ul, ol {{
                margin: 1.1em 0 1.5em;
                padding-left: 1.55em;
            }}

            li {{
                margin: 0.45em 0;
                padding-left: 0.15em;
            }}

            li::marker {{
                color: var(--accent);
                font-weight: 700;
            }}

            table {{
                width: 100%;
                margin: 2.2em 0;
                border-collapse: collapse;
                overflow: hidden;
                border: 1px solid var(--border);
                border-radius: 14px;
                font-size: 0.95em;
            }}

            thead {{
                background: var(--code-bg);
            }}

            th, td {{
                padding: 0.9em 1em;
                border-bottom: 1px solid var(--border);
                vertical-align: top;
                text-align: left;
            }}

            th {{
                color: var(--heading);
                font-weight: 700;
                letter-spacing: 0.01em;
            }}

            tr:last-child td {{
                border-bottom: 0;
            }}

            tbody tr:nth-child(even) {{
                background: rgba(127, 127, 127, 0.035);
            }}

            code {{
                color: var(--code-text);
                background: var(--code-bg);
                border: 1px solid var(--border);
                border-radius: 6px;
                padding: 0.16em 0.4em;
                font-family:
                    "SFMono-Regular",
                    Consolas,
                    "Liberation Mono",
                    Menlo,
                    monospace;
                font-size: 0.88em;
                white-space: nowrap;
            }}

            pre {{
                margin: 2em 0;
                padding: 1.2em 1.35em;
                overflow-x: auto;
                background: var(--code-bg);
                border: 1px solid var(--border);
                border-radius: 16px;
                line-height: 1.62;
            }}

            pre code {{
                padding: 0;
                color: var(--text);
                background: transparent;
                border: 0;
                white-space: pre;
                font-size: 0.9em;
            }}

            img {{
                display: block;
                max-width: 100%;
                height: auto;
                margin: 2.2em auto;
                border-radius: 16px;
                border: 1px solid var(--border);
                box-shadow: 0 14px 36px rgba(25, 22, 18, 0.10);
            }}

            figure {{
                margin: 2.2em 0;
            }}

            figcaption {{
                margin-top: -1.3em;
                color: var(--muted);
                font-size: 0.9em;
                text-align: center;
            }}

            mark {{
                color: var(--heading);
                background: rgba(213, 179, 108, 0.35);
                border-radius: 4px;
                padding: 0.05em 0.2em;
            }}

            ::selection {{
                color: var(--heading);
                background: rgba(213, 179, 108, 0.35);
            }}

            @media (max-width: 700px) {{
                body {{
                    padding: 0;
                    font-size: 16px;
                }}

                .document {{
                    min-height: 100vh;
                    border-radius: 0;
                    border-left: 0;
                    border-right: 0;
                    padding: 32px 22px;
                }}

                h1 {{
                    text-align: left;
                }}

                h1::after {{
                    margin-left: 0;
                }}

                table {{
                    display: block;
                    overflow-x: auto;
                    white-space: nowrap;
                }}
            }}

            @media print {{
                body {{
                    padding: 0;
                    background: #ffffff;
                    color: #000000;
                    font-size: 12pt;
                }}

                .document {{
                    width: 100%;
                    margin: 0;
                    padding: 0;
                    border: 0;
                    box-shadow: none;
                }}

                a {{
                    color: #000000;
                    background: none;
                    border-bottom: 1px solid #888888;
                }}

                h1, h2, h3 {{
                    break-after: avoid;
                }}

                pre, blockquote, table, img {{
                    break-inside: avoid;
                }}
            }}
        </style>
    </head>

    <body>
        <main class="document">
            {rendered_md}
        </main>
    </body>
    </html>
    """

    return html
