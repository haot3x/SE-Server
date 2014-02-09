http://pythonhosted.org/Flask-Security/customizing.html
Views
Flask-Security is packaged with a default template for each view it presents to a user. Templates are located within a subfolder named security. The following is a list of view templates:

security/forgot_password.html
security/login_user.html
security/register_user.html
security/reset_password.html
security/change_password.html
security/send_confirmation.html
security/send_login.html
Overriding these templates is simple:

Create a folder named security within your application’s templates folder
Create a template with the same name for the template you wish to override
You can also specify custom template file paths in the configuration.