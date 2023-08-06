import os

def display_on_editor(text):
    with open('.metabot2txt', 'w') as f:
        f.write(text)

    os.system('gedit .metabot2txt')


def display_list_on_editor(texts):
    if os.path.isfile('.metabot2txt'):
        os.remove('.metabot2txt')
    
    for text in texts:
        with open('.metabot2txt', 'a') as f:
            f.write(text)
            f.write('\n=====================================\n')

    os.system('gedit .metabot2txt')
