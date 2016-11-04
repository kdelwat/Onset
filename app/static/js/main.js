// Enable tooltip functionality of Bootstrap
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

// Trigger the evolve function when link is clicked
$(function() {
    $("#evolvetrigger").click(function(e) {evolve()});
});

// Request the evolved language from Flask and display it
function evolve() {
    var args = {words: $('textarea[name="word_list"]').val(),
                generations: $('input[name="generations"]').val(),
                transcriptions: $('textarea[name="transcription_list"]').val()}

    $.post('/evolve', args).done(function(evolved) {
    if (evolved['error'] != 0) {
        show_alert_box(evolved['error']);
    } else {
        $('#alert_area').hide();
        document.getElementById('rules').innerHTML = "";
        document.getElementById('words').innerHTML = "";
        document.getElementById('rules').appendChild(join_rules_array(evolved['rules'], 'Sound change rules'));
        document.getElementById('words').appendChild(create_text_area(evolved['words'], 'Evolved words'));
    }
                        }).fail(function() {
                            show_alert_box('An error occured')});
                        };

function show_alert_box(alert_text) {
    $('#alert_message').text(alert_text);
    $('#alert_area').show();
}

// Joins an array of rules into a list group within a titled panel
function join_rules_array(a, title) {
    var list = document.createElement('ul');
    list.className = "list-group";

    for (var i = 0; i < a.length; i++) {
    var item = document.createElement('li');
    item.className = "list-group-item";
    item.innerHTML = '<strong>' + a[i][0] + '</strong> ' + a[i][1] + ' &#8594; ' + a[i][2] + ' (' + a[i][3] + ')';
    list.appendChild(item);
    }
    return build_panel(list, title, false)
};

// Joins an array of text into a list group within a titled panel
function join_array(a, title) {
    var list = document.createElement('ul');
    list.className = "list-group";

    for (var i = 0; i < a.length; i++) {
    var item = document.createElement('li');
    item.className = "list-group-item";
    item.appendChild(document.createTextNode(a[i]));
    list.appendChild(item);
    }

    return build_panel(list, title, false)
};

// Creates a panel with a text area populated from a list
// of strings.
function create_text_area(populate, title) {
    var text = document.createElement('textarea');
    text.innerHTML = populate.join('\n');
    text.style = "width: 100% !important";
    text.rows = populate.length;

    return build_panel(text, title, true)
}

// Creates a panel with given title and contents
function build_panel(contents, title, body) {
    var panel = document.createElement('div');
    panel.className = "panel panel-default";
    var titleDiv = document.createElement('div');
    titleDiv.className = "panel-heading";
    var heading = document.createElement('h3');
    heading.className = "panel-title";
    heading.appendChild(document.createTextNode(title));

    titleDiv.appendChild(heading);
    panel.appendChild(titleDiv);

    if (body == true) {
    var body = document.createElement('div');
    body.className = "panel-body";
    body.appendChild(contents);
    panel.appendChild(body);
    } else {

        panel.appendChild(contents);
    };

    return panel
};

// When the window is loaded, save the automatic panel heights.
window.onload = function set_panels(){
    save_info();
    resize_panels();
};

window.onresize = resize_panels;

function save_info(){
    window.word_height = $('#word_panel').height();
    window.settings_height = $('#settings_panel').height();
};

// If the panels are side-by-side, resize them to all be the height
// of the words panel. Otherwise, set them back to the automatic heights.
function resize_panels(){
    if ( $(window).width() > 768) {
        $('#settings_panel').height(window.word_height);
    } else {
        $('#word_panel').height(window.word_height);
        $('#settings_panel').height(window.settings_height);
    }

};
