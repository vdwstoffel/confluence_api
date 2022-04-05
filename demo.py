from confluence_api import ConfluenceApi

# Create an instance of the Api
confluence = ConfluenceApi("https://you.atlissian.net/wiki", "email@email.com", "<apikey>")

# Create a new page
confluence.create_page("Page Name", "Space Key")

# Get the number of version of the page. The return will increment it by one
version = confluence.get_page_version("Page Name") + 1

# Attach files to page
confluence.create_atachment("filepath", 1)

# Edit the page
confluence.edit_page(1, "Page Name", version, "template")
