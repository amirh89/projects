{% extends "parent/base.html" %}
{% block title %}Edit User{% endblock title %}
{% block content %}

    <form method='post' enctype='multipart/form-data'>
        {% csrf_token %}
        {{ form.as_p }}
        <input type='submit' value='submit'>
    </form>

{% endblock content %}
