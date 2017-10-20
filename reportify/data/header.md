# {{ title }}

<div id="signature">
    <ul>
        {% if authors %}
        <li>
            <strong>Authors:</strong>
            {% for author in authors %}
                <a href="mailto:{{ author.email }}">{{ author.name }}</a>
                {{ ", " if not loop.last }}
            {% endfor %}
        </li>
        {% endif %}
        {% if team %}
        <li>
            <strong>Team:</strong> <span class="team">{{ team }}</span>
        </li>
        {% endif %}
        {% if created_at %}
        <li>
            <strong>Created:</strong> <span class="date">{{ created_at }}</span>
        </li>
        {% endif %}
        {% if updated_at %}
        <li>
            <strong>Updated:</strong> <span class="date">{{ updated_at }}</span>
        </li>
        {% endif %}
        {% if tags %}
        <li>
            <strong>Tags:</strong>
            {% for tag in tags %}
                <span class="tag">#{{ tag }}</span>{{ ", " if not loop.last }}
            {% endfor %}
        </li>
        {% endif %}
        {% if slug %}
        <li>
            <strong>Slug:</strong> <span class="tag">{{ slug }}</span>
        </li>
        {% endif %}
        {% if headline %}
        <li>
            <strong>Headline:</strong> <span id="headline">{{ headline }}</span>
        </li>
        {% endif %}
    </ul>
</div>
