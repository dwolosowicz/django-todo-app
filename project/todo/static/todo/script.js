$(function() {

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

    $('.tasks').on('focusout', '.content', function() {
        var task_id = $(this).parents('.task').attr('data-id');

        $(document).trigger('todo.set-content', [ task_id, $(this).text() ]);
    });

    $(document).on('todo.set-priority', function(e, task_id, level) {
        $.post('/task/priority', { id: task_id, priority: level });
    });

    $(document).on('todo.set-completed', function(e, task_id) {
        var promise = $.post('/task/completed', { id: task_id, is_completed: true });

        promise.then(function() {
            $.get(window.location.toString(), {}, function(html) {
                var $html = $(html.trim());

                $('.task-count').html($html.find('.task-count').html());
                $('.tasks').html($html.find('.tasks').html());
            });
        });
    });

    $(document).on('todo.set-content', function(e, task_id, content) {
        $.post('/task/content', { id: task_id, content: content });
    });

});
