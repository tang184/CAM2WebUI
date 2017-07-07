# Administrator Send Email
Allow admin to send email to specific users or all users.

## Set Up a new django app
Create a new app called `email_system`
  
Create a view for the email page. To make sure only admin can use this, we need to add a django decorator `@staff_member_required` before aour function.
  
First we use a form to obtain the subject, message and email:
  

In `forms.py`:
```
    from django import forms
    from django.core.validators import validate_email
    
    class MailForm(forms.Form):
        email = MultiEmailField(required=False, help_text='Split email by " ,  " or " ; ", or copy paste a list from below')
        email_all_users = forms.BooleanField(required=False)
        subject = forms.CharField(max_length=255)
        message = forms.CharField(widget=forms.Textarea)
```     
Since we want to send email to more than one address, we need to define a field that accepts multiple email addresses.
  
Before `Mailform`, add:
```
    class MultiEmailField(forms.Field):
        def to_python(self, value):
            if not value:
                return []
            #Modify the input so that email can be split by , and ;
            #For copying and pasting email address from the list, None, () \ will be removed.
            value = value.replace(' ', '') 
            value = value.replace('None,', '') 
            value = value.replace(';', ',')
            value = value.replace('(', '')
            value = value.replace(')', '')
            value = value.replace('\'', '')
            print(value)
            while value.endswith(',') or value.endswith(';'):
                value = value[:-1] #remove the last ',' or ';'

            return value.split(',')

        def validate(self, value):
            """Check if value consists only of valid emails."""
            # Use the parent's handling of required fields, etc.
            super(MultiEmailField, self).validate(value)
            for email in value:
                validate_email(email)
```
The MultiEmailField will accept a list of email addresses that is split by `,` or `;` aas well as a list copy and paste from the user info table that we will create later.
  
Now go to `views.py`:

```
    def admin_send_email(request):
        if request.method == 'POST':
            form = MailForm(request.POST)
            if form.is_valid():
                #email specific users
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                email = form.cleaned_data['email']
                email_all_users = form.cleaned_data['email_all_users'] #option for email all users
                
                try:
                    if email_all_users: #if ture, send email to all users
                        current_site = get_current_site(request)#will be used in templates
                        all_users = User.objects.all() #For iteration of email all users
                        mass_email = []
                        #iterations that add users info to each email and attach to mass_email list
                        for user in all_users: 
                            username = user.username
                            template = render_to_string('email_system/admin_send_email_template.html', {
                                'username': username,
                                'message': message,
                                'domain': current_site.domain,
                            })
                            mass_email.append((
                                subject,
                                template,
                                EMAIL_HOST_USER,
                                [user.email],
                            ))
                            
                        send_mass_mail(mass_email)
                    else: #if email_all_users is not true, send email to address that the admin typed in
                        send_mail(subject,message,EMAIL_HOST_USER,email)

                    messages.success(request, 'Email successfully sent.')#success message
                except:
                    messages.error(request, 'Email sent failed.')#error message

                return redirect('admin_send_email')
            else:
                messages.error(request, 'Email sent failed.')
        else:
            form = MailForm()
        return render(request, 'email_system/admin_send_email.html', {'form': form})
```     
There are two ways of sending email: send_mail and send_mass_mail. send_mass_mail will not close the channel of sending email after each email es sent, so it is slightly faster when sending email to a lot of people.
  
And the outcome is different. If we send_mass_email by attach every email to a list and send them together, the "to" part of the email will only show one email address, but if we use send_mail with a email list, the "to" part will show all the receivers.
  
We also used a template here for email_all_users since it is nice to have signiture for an official email:

```
    Hi {{ username }},
    {{ message }}



    Sincerely,
    CAM2
    http://{{ domain }}
```
For the convenience of administrator, it is good to have a table of all users' info.
To obtain them, we will use `objects.values` and `objects.values_list`. The `objects.values` will collect the names of each aspact of info, however, `objects.values_list` will only contain the info itself.
  
Right after `def admin_send_email(request):` and before `if request.method == 'POST':`, add the following to get user info:
  
    email_table = (User.objects.values('email')) #Obtaining a list of users' emails outside users info table for easy copying and pasting.
    users = User.objects.values_list('username', 'first_name', 'last_name', 'date_joined') #Obtaining a list of info required from user
    
and add this two lists in `return render()` in the end:
  
     return render(request, 'email_system/admin_send_email.html', {'form': form, 'users': users, 'email_table': email_table})
  
*** 
In the template, a for loop is used to display fields in the MailForm (Subject, email, message etc.), and seperate email of users from other info of users for easy copying and pasting.
  
`admin_send_email.html`

```
    {% block content %}
    <div class="top-content">
      <div class="inner-bg">
        <div class="container">
          <div class="row">
            <h3>Email Users</h3>
          </div>
            {% if messages %}
            <ul style="color: red" class="messages">
                {% for message in messages %}
                <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
                {% endfor %}
            </ul>
            {% endif %}
          <div class="form-bottom">
          <form method="post">
            {% csrf_token %}
            {% for field in form %}

                {{ field.label_tag }}<br>
                {{ field }}<br>
                {% if field.help_text %}
                    <p style="color: grey">{{ field.help_text }}</p>
                {% endif %}
                {% for error in field.errors %}
                    <p id="emailerror" style="color: red">{{ error }}</p>
                {% endfor %}

            {% endfor %}
            <button type="submit" name="sendemail" class="btn">Send</button>
            <br>
            <br>

            <div class="col-sm-3">
            <table cellspacing="2" style="width:100%; float: left">
                <tr><th>Email</th></tr>
                {% for email in email_table %}
                <tr>
                    {% if email.email%}
                        <td>{{ email.email }},</td>
                    {% else %}
                        <td>None,</td>
                    {% endif %}
                </tr>
                {% endfor %}
            </table>
            </div>
            <div class="col-sm-9">
            <table style="width:100%; float: left">
            <tr>
                <th>Username</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Date Joined</th>
            </tr>

            {% for user in users %}
                <tr>
                {% for field in user %}
                    <td>{{ field }}</td>
                {% endfor %}
                </tr>
            {% endfor %}

            </table>
            </div>
          </form>
        </div>
      </div>
    </div>
    </div>
    {% endblock %}
```

## Future improvements
  
Order the user info table by different aspect(date registered, name, etc.)

