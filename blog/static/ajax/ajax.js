$('#listbutton').click(function(){

    $.ajax({
        type:'GET',
        url:'/api/articles',
        success: function(data){

            let container = $('.alert:first').clone();
            let tag = $('.tags:first').clone()
            container.find('.tagsdiv').empty();
            $('.articlelist').empty();

            for (let idx = 0; idx < data.results.length; idx++) {
                current_data = data.results[idx];
                let clone = container.clone().css('display', '');
                clone.find('.title').text(current_data.title);

                for (let idx = 0; idx < current_data.tags.length; idx++){
                    let new_tag = tag.clone();
                    new_tag.find('.badge').text(current_data.tags[idx].name)
                    new_tag.appendTo(clone.find('.tagsdiv'))
                };

                clone.find('.content').text(current_data.content);
                clone.find('.author').text(current_data.author.username);
                clone.find('.postdate').text(current_data.post_date);
                clone.appendTo('.articlelist');

            }

        }

    })

})
