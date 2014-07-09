#coding: utf-8

from django import template

register = template.Library()


@register.simple_tag
def upload_js():
    return """
<!-- The template to display files available for upload -->
<script id="template-upload" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-upload fade">
        <td class="name" ><span>{%=file.name%}</span></td>
        <td class="type"><span>{%=file.type%}</span></td>
        {% if (file.error) { %}
            <td class="error" colspan="2"><span class="label label-danger">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else if (o.files.valid && !i) { %}
            <td>
                <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>
            </td>
            <td class="start">{% if (!o.options.autoUpload) { %}
                <button class="btn btn-success" rel="fileupload_operation">
                    <i class="glyphicon glyphicon-arrow-up icon-white"></i>
                    <span>上传</span>
                </button>
            {% } %}</td>
        {% } else { %}
            <td colspan="2"></td>
        {% } %}
        <td class="cancel">{% if (!i) { %}
            <button class="btn btn-warning" rel="fileupload_operation"
            style="height:40px">
                <i class="glyphicon glyphicon-remove icon-white"></i>
                <span>取消</span>
            </button>
        {% } %}</td>
    </tr>
{% } %}
</script>
<!-- The template to display files available for download -->
<script id="template-download" type="text/x-tmpl">
{% for (var i=0, file; file=o.files[i]; i++) { %}
    <tr class="template-download fade">
        {% if (file.error) { %}
            <td class="name" ><span>{%=file.name%}</span></td>
            <td class="type"><span>{%=file.type%}</span></td>
            <td class="error" colspan="2"><span class="label label-danger">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
        {% } else { %}
            <td class="name">
                <a href="$" title="{%=file.name%}" fid="{%=file.id%}">{%=file.name%}</a>
            </td>
            <td class="type"><span>{%=file.type%}</span></td>
            <td colspan="2"></td>
        {% } %}
        <td class="delete">
            <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}" rel="fileupload_operation">
                <i class="glyphicon glyphicon-trash icon-white"></i>
                <span>删除</span>
            </button>
        </td>
    </tr>
{% } %}
</script>
"""
