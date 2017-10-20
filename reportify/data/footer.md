## Links

<div id="report-footer">
    {% if report_link %}
    <p>Files used to generate data, do this analysis and make this document:</p>
    <p><a href="{{ report_link }}">{{ report_link }}</a></p>
    {% endif %}

    {% if plug %}
    <p>This report was generated automatically from a Jupyter notebook using <a href="https://github.com/eddiejessup/reportify" target="_blank">Reportify</a>.</p>
    {% endif %}
</div>
