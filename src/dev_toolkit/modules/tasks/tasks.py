import datetime
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from pathlib import Path

from src.dev_toolkit.config.app_config import APP_PATHS

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
        md_content += f'* **Required by:** <span class="{task["required_by"].lower()}">{task["required_by"]}</span>\n'
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
        extensions=['extra', 'sane_lists', 'smarty', 'toc', 'attr_list', TargetBlankExtension()],
        output_format='html5'
    )
    
    filename = Path(APP_PATHS.get('TASK_TEMPLATE', ''))
    with open(filename, encoding='utf-8') as f:
        template = f.read()
        
    html = (
        template
        .replace('{{title}}', 'Tareas pendientes')
        .replace('{{eyebrow}}', 'INFORME')
        .replace('{{subtitle}}', datetime.datetime.now().isoformat())
        .replace('{{footer_left}}', 'Documento generado automáticamente por DevToolkit')
        .replace('{{footer_right}}', '')
        .replace('{{content}}', rendered_md)
    )
    
    return html
