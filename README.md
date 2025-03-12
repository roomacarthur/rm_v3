# RM_v3 - Portfolio & Blog

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Deployed on Railway](https://img.shields.io/badge/Deployed%20on-Railway-blue.svg)](https://railway.com?referralCode=roomacarthur)

[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](https://github.com/roomacarthur/rm_v3/actions)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)


Welcome to **RM_v3**, a modern portfolio website and blog built with Django that showcases my projects, skills, and the work I’m passionate about. This project highlights a range of web development skills—from dynamic content rendering using Markdown to leveraging modern tools like HTMX for an enhanced user experience.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Live Demo](#live-demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

**RM_v3** is a personal portfolio and blog site that not only showcases my past projects but also demonstrates cutting-edge web development techniques. The site is structured around two primary Django apps:

- **Blog App**:  
  - A rich, searchable blog with filtering by categories and hashtags.
  - Supports HTMX for partial updates, offering a snappy and dynamic user experience.
  
- **Portfolio App**:  
  - A comprehensive display of my projects.
  - Each project supports detailed Markdown-rendered content, multiple technologies, and status indicators (complete/incomplete) to help manage what’s live.
  - Projects not marked as complete automatically redirect to the portfolio list.

## Features

- **Dynamic Content Rendering**:  
  Render rich content from Markdown with syntax highlighting and tables.

- **HTMX Integration**:  
  Enhance user experience with partial page updates.

- **Robust Filtering & Search**:  
  Easily search blog posts by title, hashtags, or category.

- **Responsive Design**:  
  Beautifully crafted templates that work on both desktop and mobile devices.

- **Pagination**:  
  Both the blog and portfolio listings are paginated for a seamless browsing experience.

- **Third-Party Integrations**:  
  - **Cloudinary** for image hosting.
  - **ColorField** for dynamic color styling.
  
## Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) (Python)
- **Frontend**: HTML5, CSS3, Bootstrap (or your custom styles)
- **Templating**: Django Templates, with HTMX for dynamic content updates
- **Database**: SQLite (by default) — easily switchable to PostgreSQL or another RDBMS
- **Media**: [Cloudinary](https://cloudinary.com/) for image management
- **Markdown Processing**: [Markdown](https://python-markdown.github.io/) with extensions for code highlighting and tables

## Live Demo

Check out the live demo of the portfolio site here: [Your Live URL Here](https://www.roomacarthur.dev/)

## Installation

Follow these steps to get the project running locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/roomacarthur/rm_v3.git
   cd rm_v3
