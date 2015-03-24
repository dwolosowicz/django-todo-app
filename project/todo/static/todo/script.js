$(function() {
    var _state = {};

    $('.tasks').on('click', '.task-priority', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        var priorities = [
            {
                class: 'task-priority-low',
                key: 'L'
            },
            {
                class: 'task-priority-normal',
                key: 'N'
            },
            {
                class: 'task-priority-high',
                key: 'H'
            }
        ];

        for(var i = 0; i < priorities.length; i += 1) {
            if(!$(this).hasClass(priorities[i].class)) {
                continue;
            }

            var newIndex = i + 1;

            if(i > priorities.length - 2) {
                newIndex = 0;
            }

            $(this).removeClass(priorities[i].class);
            $(this).addClass(priorities[newIndex].class);

            $(document).trigger('todo.set-priority', [ task_id, priorities[newIndex].key ])

            return;
        }
    });

    $('.tasks').on('click', '.finish', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        $(document).trigger('todo.set-completed', [ task_id ]);
    });

    $('.tasks').on('click', '.remove', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        $(document).trigger('todo.remove', [ task_id ]);
    });

    $('.tasks').on('focus', '.content', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        _state['task-' + task_id] = { content: $(this).html() };
    });

    $('.tasks').on('focusout', '.content', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        if(_state['task-' + task_id].content !== $(this).html()) {
            $(document).trigger('todo.set-content', [ task_id, $(this).text() ]);
        }
    });

    $(document).on('todo.set-priority', function(e, task_id, level) {
        promise = $.post('/task/priority', { id: task_id, priority: level });

        promise.then(function() {
            $(document).trigger('todo.reload', [ '.task[data-id=' + task_id + '] em', false ]);
        });
    });

    $(document).on('todo.remove', function(e, task_id) {
        var promise = $.post('/task/remove', { id: task_id });

        promise.then(function() {
            $(document).trigger('todo.reload');
        });
    });

    $(document).on('todo.set-completed', function(e, task_id) {
        var promise = $.post('/task/completed', { id: task_id, is_completed: true });

        promise.then(function() {
            $(document).trigger('todo.reload');
        });
    });

    $(document).on('todo.set-content', function(e, task_id, content) {
        var promise = $.post('/task/content', { id: task_id, content: content });

        promise.then(function() {
            $(document).trigger('todo.reload', [ '.task[data-id=' + task_id + '] .task-body' ]);
        });
    });

    $(document).on('todo.reload', function(e, customDomId, animate) {
        var domId = '.tasks';

        if(typeof animate == 'undefined') {
            animate = true;
        }

        if(typeof customDomId != 'undefined') {
            domId = customDomId;
        }

        var reloadCallback = function() {
            $.get(window.location.toString(), {}, function(html) {
                var $html = $(html.trim());

                $('.task-count').html($html.find('.task-count').html());

                $(domId).html($html.find(domId).html());

                if(animate) {
                    $(domId).fadeIn('normal');
                }
            });
        }

        if(animate) {
            $(domId).fadeOut('fast', reloadCallback);
        } else {
            reloadCallback();
        }
    });

});
