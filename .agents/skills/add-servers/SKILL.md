# MCP Servers
Backend Internal api's url: https://github.com/druling/backend/tree/dev/apps/internal/integrations

This skills is for adding new servers to MCP, below we define the folder structure and files to be added.

## File Structure
* servers
  * path: src/servers
  * Here we add the server code for the service we want to integrate, for example if we want to integrate a service called "example_service" we will add a folder "example_service" in src/servers and add the relevant code for that service in that folder.
  * Ex:
    * src/servers/example_service/
      * __init__.py
      * mcp.py (this file will contain the code to interact with the service's api) 
      * prompts.py (this file will contain the prompts for the service)
  * Once the server is added register it in src/servers/__init__.py by importing the mcp.py file and adding it to the MCP factory map.

## Checklist
When asked to add a service to integration please 

- [ ] Understand the api's from backend repo and the data required to integrate the service.
- [ ] Ask if there are any specific fun's the user wants.
- [ ] See all the file structure
- [ ] add relevant files, folder enums for that particular service. 
