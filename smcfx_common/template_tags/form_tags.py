from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'

    if bound_field.field.widget.__class__.__name__.lower().find('checkboxinput') >= 0:
        return css_class

    tmp_class = ''
    if bound_field.field.widget.attrs.get('class') is not None:
        tmp_class = bound_field.field.widget.attrs.get('class')

    return 'form-control {} {}'.format(css_class, tmp_class)


@register.filter
def li_class(bound_field):
    ftype = bound_field.field.widget.__class__.__name__
    maxLength = 0
    tmp_class = None
    if bound_field.field.widget.attrs.get('class') is not None:
        tmp_class = bound_field.field.widget.attrs.get('class')
        tmp_class = list(map(lambda x: x.lower().strip(), tmp_class.split(' ')))
    if tmp_class is not None:
        if 'li-small-box' in tmp_class:
            return 'small-box'
        elif 'li-middle-box' in tmp_class:
            return 'middle-box'
        elif 'li-big-box' in tmp_class:
            return 'big-box'
    if ftype.lower() == 'TextInput'.lower():
        try:
            maxLength = int(bound_field.field.max_length)
        except:
            maxLength = 5000
        if maxLength is None or maxLength <= 100:
            return 'small-box'
        elif maxLength > 100 and maxLength <= 250:
            return 'middle-box'
        else:
            return 'big-box'
    elif ftype.lower() == 'textarea':
        return 'big-box'
    elif ftype.lower() == 'select':
        return 'small-box'
    elif ftype.lower() == 'numberinput' or ftype.lower() == 'timeinput' :
        return 'small-box'
    elif ftype.lower() == 'checkboxinput':
        return 'small-box'
    elif ftype.lower() == 'checkboxselectmultiple':
        return 'middle-box'
    else:
        raise Exception(ftype.lower())



@register.filter
def trans_error(err_string):
    if err_string.strip() == "A user is already registered with this e-mail address.":
        return "ایمیل وارد شده در سامانه وجود دارد."
    elif err_string.strip() == "A user with that username already exists.":
        return "نام کاربری در سامانه وجود دارد."
    elif err_string.strip() == "This password is entirely numeric.":
        return "کلمه عبور نباید کاملا عددی باشد."
    elif err_string.strip() == "This password is too short. It must contain at least 8 characters.":
        return "کلمه عبور باید حداقل ۸ کارکتر باشد."
    elif err_string.strip() == "You must type the same password each time.":
        return "کلمه عبور و تکرار آن با هم مطابقت ندارند."
    return err_string



@register.simple_tag
def setvar(val=None):
    return val
