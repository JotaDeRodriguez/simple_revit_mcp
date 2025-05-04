# Simple Revit MCP implementation

### A minimal and beginner friendly implementation of the MCP protocol for Autodesk Revit.

---

**Why?**

- After being frustrated with the multiple MCP for Revit implementations floating around the internet, I decided that I wanted to try my hand at providing a simple, pyRevit oriented MCP implementation. 

**How?**

- This minimal implementation works by using the Routes module inside of pyRevit. It is aimed at providing you a very simple template to get started, from which you can very quickly prototype and iterate tools and methods to give access an LLM access to your Revit Model. 
- These very simple tools are meant to be expanded to your usecase, and you're very welcome to fork the repo and make your own contributions.
- In terms of production use, be adviced that the pyRevit Routes API is a draft, and subject to change. It lacks any authentication mechanism so if you need it, you'll have to implement it yourself. If this repo were to break unexpectedly in the future, maybe I'll get around to fix it.


**Batteries included**

- This repo is aimed at beginners or Python specialists who aren't versed in C#, or who want to prototype and iterate quickly. It shall include the full Routes implementation, a minimal MCP script to connect to an MCP-compatible client, and a few test commands to get started.

