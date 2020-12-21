import bs4
from urllib.parse import urlparse
from urllib.request import urlopen
import os
import sys
from ebooklib import epub

BASEPATH = '.'

def create_chapter(name, address, uid):
	url = urlparse(address)
	directory = BASEPATH+url.path
	filename = os.path.join(directory, 'index.html')
	print(f"Reading {name} from {filename}")
	if not os.path.exists(filename):
		os.makedirs(directory, exist_ok=True)
		print(f"fetching {address}")
		raw = urlopen(address).read()
		with open(filename, 'wb') as f:
			f.write(raw)
	with open(filename) as f:
		raw = f.read()
	soup = bs4.BeautifulSoup(raw, 'lxml')
	title = soup.select_one('.entry-title').text
	text = soup.select_one('.entry-content').find_all('p')
	for p in text:
		while p.span:
			p.span.unwrap()
	text.insert(0,f"<h1>{title}</h1>")
	epubhtml = epub.EpubHtml(title=title, file_name=f"ch{uid}.xhtml")
	content = ''.join(map(str,text))
	epubhtml.set_content(content)
	return epubhtml

class Book:
	def __init__(self, name, uid):
		self.name = name
		self.uid = uid
		self.chapters = []
	def add_chapters(self,li):
		for n,l in enumerate(li):
			a=l.find('a')
			self.chapters.append(create_chapter(name=a.text, address=a.attrs['href'], uid=uid*1000+n))

try:
	volume = sys.argv[1]
except IndexError:
	volume = None
f=urlopen("https://practicalguidetoevil.wordpress.com/table-of-contents/")
#with open('table-of-contents/index.html') as f:
toc = bs4.BeautifulSoup(f.read(),'lxml').select('.entry-content')[0]
books = []
uid = 0
for child in toc.children:
	if child.name == 'h2':
		uid += 1
		if volume:
			if int(volume)!=uid:
				continue
		books.append(Book(child.text, uid=uid))
	if child.name == 'ul':
		if volume:
			if int(volume)!=uid:
				continue
		print(uid)
		books[-1].add_chapters(child.find_all('li'))

for b in books:
	book = epub.EpubBook()

	book.set_identifier(f'apgte-{b.uid}')
	book.set_title(f'A Practical Guide to Evil - {b.name}')
	book.set_language('en')

	book.add_author('ErraticErrata')
	book.spine = ['nav']
	chapters_in_book = []
	for c in b.chapters:
		book.add_item(c)
		chapters_in_book.append(c)
	book.toc.append((epub.Section(b.name),chapters_in_book))
	book.spine.extend(chapters_in_book)
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())
	epub.write_epub(f"apgte{b.uid}.epub", book)
