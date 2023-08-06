import gitlab
import git


class GitlabWikiPage():
    def __init__(self, gitlab_url, private_token, project_name, page_name):
        try:
            # gitlab auth
            gl = gitlab.Gitlab(gitlab_url, private_token)
            self._gitlab_obj = gl.auth()
        except Exception as e:
            print('gitlab auth failed because {}'.format(e))
            self._gitlab_obj = None
            
        
        # the project where contains all pages need
        self._doc_project = gl.projects.get(project_name)
        # page where we need update content
        try:
            self._publish_page = self._doc_project.wikis.get(page_name)
        except Exception as e:
            print("Page {} doesn't existed, create new page")
            self._publish_page = self._doc_project.wikis.create({
                    'title': page_name,
                    'content': "Empty page"
            })
            
        # init section
        self.list_sections = []
        
    def add_section(self, section):
        self.list_sections.append(section)
        
    def render(self):
        content = ""
        for section in self.list_sections:
            content += section.render()
            
        return content
            
    def publish(self):
        try:
            self._publish_page.title = self._publish_page.title
            self._publish_page.content = self.render()
            self._publish_page.save()
        except Exception as e:
            print('Publish failed because {}'.format(e))
            
    def toMd(self, md_filename):
        md_file = open('{}.md'.format(md_filename), 'w')
        md_file.write(self.render())
        md_file.close()
            

class Section():
    def __init__(self, section_name):
        self._content = '# {}'.format(section_name)+"\n\n"

    def description(self, description):
        self._content += description+"\n\n"

    def heading(self, text, level=1):
        self._content += '{} {} {}'.format('#'*level, text, '#'*level)+"\n"
        
    def multi_content_part(self, list_content_parts):
        for content_part in list_content_parts:
            self._content += content_part+"\n\n"

    def block(self, block):
        self._content += '``` {} ```'.format(block)+"\n\n"

    def table(self, two_dimentional_list):
        self._content += "|" + "|".join(two_dimentional_list[0]) + "|\n"
        self._content += "|" + "-|"*len(two_dimentional_list[0]) + "\n"
        for i in range(1, len(two_dimentional_list)):
            self._content += "|" + "|".join(list(map(lambda x: str(x), two_dimentional_list[i]))) + '|\n'
            
    def df_to_table(self, pd_df):
        self._content += "|" + "|".join(pd_df.columns) + "|\n"
        for index, row in pd_df.iterrows():
            if index == 0:
                self._content += "|" + "-|"*len(row) + "\n"

            self._content += "|" + "|".join(list(map(lambda x: str(x), row))) + '|\n'
            
    def checked_list(self, list_check, checked_indexes=[0]):
        for i in range(0, len(list_check)):
            if i in checked_indexes:
                self._content += '- [x] {}'.format(list_check[i]) + '\n'
            else:
                self._content += '- [ ] {}'.format(list_check[i]) + '\n'

    def hyperlink(self, text, link):
        self._content += HelperDocs.hyper(text, link)+"\n"

    def li(self, li):
        self._content += '* {}'.format(li)+"\n\n"
        
    def image(self, img_url, alt='default alt'):
        self._content += '![{}]({})'.format(alt, img_url)+"\n\n"
        
    def set_content(self, content):
        # can use to set section content
        self._content = content

    def render(self):
        return self._content
    

class HelperDocs():
    def get_tag(style):
        TAGS = {
            'bold': '**',
            'italic': '*',
            'strike-throught': '~~'
        }
        
        return TAGS[style] if style in TAGS.keys() else ''
    
    def text(text, style='bold'):
        tag = HelperDocs.get_tag(style)
        return '{}{}{}'.format(tag, text, tag)
        
    def text_combine(text, styles=[]):
        tags = [HelperDocs.get_tag(style) for style in styles]
        return '{}{}{}'.format(''.join(tags), text, ''.join(tags))
        
    def hyper(text, link):
        return '[{}]({})'.format(text, link)