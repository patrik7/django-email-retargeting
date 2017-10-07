=====
Email Retargetting
=====

Email Retargeting is a simple app that allows to defer email sends. Emails can be templated using django admin, so can be used directly be less tech-savy people.

Emails are sent right away or later, when:

-Batch job runs
-Specific date
-Specific condition

App allows for use-cases like: send this email in 3 days if user has not performed an action.

Email are send thru django email subsyetm that can be hooked to any SMTP service, like mailgun.

You need to set up django SMTP subsystem as usual:
https://docs.djangoproject.com/en/1.11/topics/email/#smtp-backend

django-email-retargeting will populate in your django admin interface, where you can create email templates, see sent emails, and manage emails that are going ot be sent.

Quick start
-----------

1. Add "django-email-retargeting" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-email-retargeting',
    ]

2. Run `python manage.py migrate` to create the models.

To send an email::

    schedule_send_email(
        "register_follow_up_1", #campaign name, to match the right template, can be created thru admin
        user.email, #receiver email
        'example.com', #sender domain / used to compile absolute URLs in the email
        {}, #dictionary, django's rendering is used
        send_after=timezone.now() + timedelta(days=1), #OPTIONAL: send after this time
        send_condition=condition #OPTIONAL: send if condition is met / otherwise drop
     )

3. To execute scheduled sends: `python manage flush_queue`

