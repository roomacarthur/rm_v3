---
meta_title: "How To: Setting up 'robots.txt' in your Django Project"
meta_description: "Learn how to set up and configure a robots.txt file in your Django project to manage web crawlers and optimize your site's SEO."
meta_keywords: ["Django robots.txt", "robots.txt tutorial", "SEO Django", "Django web crawlers", "Django configuration"]
---

# How To: Setting up 'robots.txt' in your Django Project

When building a Django web application, managing how search engines and web crawlers interact with your site is critical for search engine optimization (SEO). One of the simplest ways to control this is through a `robots.txt` file. In this guide, I'll walk you through setting up `robots.txt` in your Django project step-by-step.

---

## What is `robots.txt`?

The `robots.txt` file is a plain text file that tells search engine crawlers which parts of your site should or should not be indexed. It’s placed at the root of your website (e.g., `https://roomacarthur.dev/robots.txt`). 

A basic `robots.txt` file might look like this:

```txt
User-agent: *
Disallow: /admin/
Allow: /
```

- **`User-agent`** specifies which crawlers the rules apply to (e.g., Googlebot, Bingbot).
- **`*`** specifies a wildcard, in the above example this relates to all crawlers. 
- **`Disallow`** specifies paths that crawlers should avoid.
- **`Allow`** specifies paths that crawlers can access (useful for exceptions within disallowed paths).

---

## Steps to Set Up `robots.txt` in Django

Here’s how to add a `robots.txt` file to your Django project:

### Step 1: Create the `robots.txt` File

Start by creating a `robots.txt` file in your project’s root template directory. For example:

1. In the root of your project you should have a `templates/` directory, in most cases this is where your html file that you extend will be located, I usually call mine `base.html`. 

2. Add the following content to the file:

    ```txt
    User-agent: *
    Disallow: /admin/
    Allow: /
    ```

Modify the contents to match your site’s requirements.

---

### Step 2: Configure Django to Serve Static Files

To serve the `robots.txt` file, ensure your Django project is set up to handle static files correctly:

1. Open your `settings.py` file and verify the `STATIC_URL` and `STATICFILES_DIRS` settings:

    ```python
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    ```

2. Place the `robots.txt` file in the static folder of your project. The path should look like `static/robots.txt`.

3. During development, Django’s static file handling will automatically serve this file.

---

### Step 3: Verify the File in Development

Run your development server and visit `http://127.0.0.1:8000/static/robots.txt`. You should see the contents of your `robots.txt` file displayed in plain text.

If you want the file to be accessible directly at `http://127.0.0.1:8000/robots.txt`, you can create a URL pattern to serve it:

1. In your `urls.py`, add the following:

    ```python
    from django.urls import re_path
    from django.views.generic import TemplateView

    urlpatterns = [
        # Other URLs
        re_path(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    ]
    ```

2. Move the `robots.txt` file to your templates directory.

---

### Step 4: Deploy to Production

When deploying your Django project, ensure that your web server (e.g., Nginx or Apache) is configured to serve the `robots.txt` file from the project’s static files. This typically involves:

1. Collecting static files:

    ```bash
    python manage.py collectstatic
    ```

2. Configuring the web server to serve the `robots.txt` file from the `STATIC_ROOT` directory.

---

## Best Practices for `robots.txt`

1. **Be Specific:** Only disallow sensitive or unnecessary parts of your site. For example:

    ```txt
    User-agent: *
    Disallow: /private-data/
    Disallow: /temp/
    Allow: /
    ```

2. **Don’t Rely Solely on `robots.txt`:** It’s a suggestion, not a rule. Sensitive data should always be protected with proper authentication.

3. **Use Sitemap Directives:** Include a reference to your XML sitemap to help crawlers find your content:

    ```txt
    Sitemap: https://example.com/sitemap.xml
    ```

4. **Test Regularly:** Use tools to validate your `robots.txt` file and ensure it’s working as intended.

---

## Conclusion

Setting up a `robots.txt` file in your Django project is straightforward and an essential step for SEO and managing web crawlers. By following the steps outlined above, you can easily control how search engines interact with your site, ensuring better performance and security.

For more Django tutorials, check out our [Django Basics Series](#). Got questions? Drop them in the comments below!

