def render_task_md(tasks: list[dict]) -> str:
    md_content = ''
    
    pending_tasks = [task for task in tasks if not task['done']]
    done_tasks = [task for task in tasks if task['done']]
    
    for n_task, task in enumerate(pending_tasks):
        md_content += f'## {n_task + 1}. {task["name"]}\n'
        md_content += f'* **Date:** {task["addition_date"]}\n'
        if task['ticket']:
            md_content += f'* **Ticket:** '
            md_content += f'[#{task["ticket"]}]'
            md_content += f'(https://tickets.inescop.es/scp/tickets.php?a=search&search-type=&query={task["ticket"]})\n'
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
        md_content += f'* *[{task["done"]}] {task["name"]}*'
    
    return md_content