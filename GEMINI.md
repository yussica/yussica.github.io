# Gemini

This document explains how to use Gemini to interact with this project.

## Setup

To use Gemini with this project, you will need to:

1.  Install the Gemini CLI.
2.  Authenticate with your Google account.
3.  Set the project context to this directory.

## Usage

Once you have set up Gemini, you can use it to interact with the blog in a variety of ways.

### Creating Content

To create a new blog post, you can use the following command:

```
gemini "Create a new blog post titled 'My New Post' with the content 'This is my new post.'"
```

Gemini will then create a new markdown file in the `_posts` directory with the specified title and content.

### Editing Content

To edit an existing blog post, you can use the following command:

```
gemini "Edit the blog post 'My New Post' to say 'This is my updated post.'"
```

Gemini will then update the content of the specified blog post.

### Managing the Site

You can also use Gemini to manage the site's configuration. For example, to add a new link to the navigation bar, you can use the following command:

```
gemini "Add a new link to the navigation bar with the title 'My New Link' and the URL '/my-new-link/'"
```

Gemini will then update the `_config.yml` file to add the new link.
